from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.modelAdminRegister import AdminRegister
from app.schemas.schemasAdminRegister import CreateRegistration, LoginAdmin
import os
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token
from app.core.dependency import get_current_user
import shutil
from app.models.modelCustomerRegistration import ModelCustomerRegistration,BoreWellInfo


def get_admin_id_from_file():
    admin_id = os.getenv("BOREWELL_SERVICE_ADMIN_ID")
    
    if not admin_id:
        raise ValueError("Admin ID not found in environment variables")
    
    return admin_id.strip()

    
def create_admin(db:Session, user:CreateRegistration):
    admin_id=get_admin_id_from_file()

    if user.new_password != user.confirm_password:
        raise ValueError("passwords do not match")
    
    if db.query(AdminRegister).filter(AdminRegister.email == user.email).first():
        raise ValueError("email already exists")
    
    if user.admin_id != admin_id:
        raise HTTPException(status_code=400, detail="Invalid admin ID")    
    hashed_password=hash_password(user.new_password)

    db_user=AdminRegister(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_admin(db:Session, credentials:LoginAdmin):
    user=db.query(AdminRegister).filter(AdminRegister.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email ")
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid  password")
    
    token=create_access_token(user_id=user.id, role=user.role)

    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}


def get_admin(db:Session):
    return db.query(AdminRegister).all()


#delete the admin
def delete_admin(db:Session, admin_id:int):

    admin=db.query(AdminRegister).filter(AdminRegister.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted successfully"}


def send_borewell_info(db: Session, customer_num: str, bore: BoreWellInfo):

    customer = db.query(ModelCustomerRegistration).filter(
        ModelCustomerRegistration.phoneNumber == customer_num
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    borewell_info = BoreWellInfo(
        customer_id=customer.id,
        borewell_depth=bore.borewell_depth,
        phoneNumber=customer.phoneNumber,
        casing_depth=bore.casing_depth,
        water_level=bore.water_level,

        # Pipe details
        pipe_size=bore.pipe_size,
        pipe_joint=bore.pipe_joint,

        # Structural details
        water_gaps=bore.water_gaps,
        casing_Condition=bore.casing_Condition,
        pipe_Condition=bore.pipe_Condition,

        # Water quality (manual input)
        Water_Quality=bore.Water_Quality,

        # Water test values
        tds=bore.tds,
        ph=bore.ph,
        hardness=bore.hardness,
        iron=bore.iron,
        chlorine=bore.chlorine,
        nitrate=bore.nitrate,

        # Visual checks
        water_color=bore.water_color,
        water_smell=bore.water_smell,

        # Final result
        water_quality_status=bore.water_quality_status
    )

    db.add(borewell_info)
    db.commit()
    db.refresh(borewell_info)

    return borewell_info



#analyzing the borewell data and giving recommendation
def get_product_recommendations(analysis):
    issues = analysis["issues"]

    drinking = {"low": [], "medium": [], "high": []}
    bathing = {"low": [], "medium": [], "high": []}
    washing = {"low": [], "medium": [], "high": []}

    # --- DRINKING ---
    if any("TDS" in i or "nitrate" in i or "Acidic" in i for i in issues):
        drinking["low"].append("Basic RO purifier")
        drinking["medium"].append("RO + UV water purifier")
        drinking["high"].append("RO + UV + Mineral booster purifier")

    if any("iron" in i for i in issues):
        drinking["medium"].append("RO + Iron removal filter")
        drinking["high"].append("Advanced iron removal + RO system")

    # --- BATHING ---
    if any("Hard water" in i or "chlorine" in i for i in issues):
        bathing["low"].append("Tap shower filter")
        bathing["medium"].append("Bathroom water softener")
        bathing["high"].append("Whole house water softener")

    # --- WASHING ---
    if any("iron" in i for i in issues):
        washing["low"].append("Basic iron filter")
        washing["medium"].append("Iron removal filter system")
        washing["high"].append("Automatic iron removal plant")

    if any("Hard water" in i for i in issues):
        washing["medium"].append("Water softener")
        washing["high"].append("Full house softener system")

    return {
        "drinking": drinking,
        "bathing": bathing,
        "washing": washing
    }

def analyze_and_recommend(bore):
    issues = []
    solutions_low = set()
    solutions_medium = set()
    solutions_high = set()

    # --- TDS ---
    if bore.tds:
        if bore.tds > 1000:
            issues.append("Very high TDS (unsafe)")
        elif bore.tds > 500:
            issues.append("High TDS")

        if bore.tds > 500:
            solutions_low.add("Use for washing, not drinking")
            solutions_medium.add("Install RO purifier")
            solutions_high.add("Advanced RO with mineral controller")

    # --- pH ---
    if bore.ph:
        if bore.ph < 6.5:
            issues.append("Acidic water")
            solutions_medium.add("RO purifier with pH balance")
            solutions_high.add("Automatic pH balancing system")
        elif bore.ph > 8.5:
            issues.append("Alkaline water")
            solutions_medium.add("RO purifier")

    # --- Hardness ---
    if bore.hardness and bore.hardness > 200:
        issues.append("Hard water")
        solutions_low.add("Use detergent/anti-scale agents")
        solutions_medium.add("Install water softener")
        solutions_high.add("Whole-house softener system")

    # --- Iron ---
    if bore.iron and bore.iron > 1:
        issues.append("High iron content")
        solutions_low.add("Basic iron filter (temporary)")
        solutions_medium.add("Iron removal filter")
        solutions_high.add("Automatic iron removal plant")

    # --- Nitrate ---
    if bore.nitrate and bore.nitrate > 50:
        issues.append("High nitrate (unsafe for drinking)")
        solutions_low.add("Avoid drinking")
        solutions_medium.add("RO purifier (essential)")
        solutions_high.add("Advanced RO system with nitrate removal")

    # --- Chlorine ---
    if bore.chlorine and bore.chlorine > 0.5:
        issues.append("High chlorine")
        solutions_low.add("Store water before use")
        solutions_medium.add("Carbon filter")
        solutions_high.add("Multi-stage filtration system")

    # --- Final Status ---
    if not issues:
        status = "Good"
        color = "green"
    elif len(issues) <= 2:
        status = "Average"
        color = "yellow"
    else:
        status = "Bad"
        color = "red"

    return {
        "status": status,
        "color": color,
        "issues": issues,
        "solutions": {
            "low_cost": list(solutions_low),
            "medium_cost": list(solutions_medium),
            "high_cost": list(solutions_high),
        }
    }

def get_borewell_info(db: Session, customer_num: str):
    borewell_list = db.query(BoreWellInfo).filter(
        BoreWellInfo.phoneNumber == customer_num
    ).all()

    if not borewell_list:
        raise HTTPException(
            status_code=404,
            detail="Borewell information not found for the customer"
        )

    final_response = []

    for bore in borewell_list:
        analysis = analyze_and_recommend(bore)

        # 🔥 NEW: product suggestions
        product_suggestions = get_product_recommendations(analysis)

        final_response.append({
            "borewell_data": {
                "borewell_depth": bore.borewell_depth,
                "casing_depth": bore.casing_depth,
                "water_level": bore.water_level,
                "pipe_size": bore.pipe_size,
                "pipe_joint": bore.pipe_joint,
                "water_gaps": bore.water_gaps,
                "casing_Condition": bore.casing_Condition,
                "pipe_Condition": bore.pipe_Condition,
                "Water_Quality": bore.Water_Quality,
                "tds": bore.tds,
                "ph": bore.ph,
                "hardness": bore.hardness,
                "iron": bore.iron,
                "chlorine": bore.chlorine,
                "nitrate": bore.nitrate,
                "water_color": bore.water_color,
                "water_smell": bore.water_smell
            },
            "analysis": analysis,
            "recommendations": product_suggestions   # 👈 NEW FIELD
        })

    return final_response








