from fastapi import APIRouter, HTTPException, Query, Body, Depends, status
from pymongo.errors import DuplicateKeyError
from models.employee import Employee
from config.db import employees_collection


from config.db import employees_collection
from utils.auth_utils import get_current_user
from models.auth import UserInDB

router = APIRouter()



# Helper to convert ObjectId to str
def serialize_employee(employee: dict) -> dict:
    employee["_id"] = str(employee["_id"])
    return employee



# Protected Create Employee by admin only
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: Employee, current_user: UserInDB = Depends(get_current_user)):
    if not current_user:   
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access. Please log in.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        result = await employees_collection.insert_one(employee.dict())
        new_employee = await employees_collection.find_one({"_id": result.inserted_id})
        return serialize_employee(new_employee)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Employee ID already exists")



# Average Salary by Department
@router.get("/avg-salary")
async def average_salary_by_department():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"_id": 0, "department": "$_id", "avg_salary": {"$round": ["$avg_salary", 2]}}},
    ]
    result = await employees_collection.aggregate(pipeline).to_list(length=100)
    return result



# Search Employees by Skill
@router.get("/search")
async def search_employees_by_skill(skill: str = Query(..., description="Skill to search for")):
    query = {"skills": {"$in": [skill]}}
    employees_cursor = employees_collection.find(query)
    employees = await employees_cursor.to_list(length=100)
    return [serialize_employee(emp) for emp in employees]



# Get Employee by ID
@router.get("/{employee_id}")
async def get_employee_by_emp_id(employee_id: str):
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return serialize_employee(employee)



# Protected Update Employee by admin 
@router.put("/{employee_id}")
async def update_employee(
    employee_id: str,
    updates: dict = Body(...),
    current_user: UserInDB = Depends(get_current_user)
):
    if not current_user:   
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access. Please log in.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    
    if "employee_id" in updates:
        raise HTTPException(status_code=400, detail="Cannot update employee_id")
    
    result = await employees_collection.update_one(
        {"employee_id": employee_id}, {"$set": updates}
    )
    
    updated_employee = await employees_collection.find_one({"employee_id": employee_id})
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return serialize_employee(updated_employee)




# Protected Delete Employee by admin 
@router.delete("/{employee_id}")
async def delete_employee(employee_id: str,current_user: UserInDB = Depends(get_current_user)):
    if not current_user:   
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access. Please log in.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = await employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"detail": f"Employee {employee_id} deleted successfully"}



# List Employees by Department with Pagination
@router.get("/")
async def list_employees_by_department(
    department: str = Query(None, description="Filter by department"),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page (max 100)")
):
    """
    Returns a paginated list of employees.
    - department: optional filter by department
    - page: page number (default 1)
    - page_size: number of records per page (default 10, max 100)
    """
    query = {"department": department} if department else {}

    # Calculate skip
    skip = (page - 1) * page_size

    # Fetch paginated employees
    employees_sorted = (
        employees_collection.find(query)
        .sort("joining_date", -1)
        .skip(skip)
        .limit(page_size)
    )
    employees = await employees_sorted.to_list(length=page_size)

    # Total documents and total pages
    total_count = await employees_collection.count_documents(query)
    total_pages = (total_count + page_size - 1) // page_size

    return {
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages,
        "employees": [serialize_employee(emp) for emp in employees],
    }

