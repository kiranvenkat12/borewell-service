from sqlalchemy.orm import Session
from app.models.modelServiceRequest import MOdelServiceRequest
from app.schemas.schemasServiceRequest import CreateSchemasServiceRequest, ResponseSchemasServiceRequest
from datetime import datetime
from fastapi import HTTPException
from app.models.modelWorkerRegister import ModelWorkerRegister
import math

def create_service_request(db:Session, service_request:CreateSchemasServiceRequest):
    db_service_request=MOdelServiceRequest(
 
        name=service_request.name,
        phone_primary=service_request.phone_primary,
        phone_secondary=service_request.phone_secondary,
        
        service_type=service_request.service_type,
        borewell_depth=service_request.borewell_depth if service_request.borewell_depth else None,

        address=service_request.address,
        
        pincode=service_request.pincode,
        description=service_request.description,
        status="Pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()

    )
    db.add(db_service_request)
    db.commit()
    db.refresh(db_service_request)
    return db_service_request


def get_service_request(db: Session, service_request_id: int):
    service_request = db.query(MOdelServiceRequest).filter(
        MOdelServiceRequest.id == service_request_id
    ).first()

    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")

    return service_request


def get_all_service_requests(db: Session):
    return db.query(MOdelServiceRequest).all()


# It will assign the worker
def assign_worker(db:Session, service_request_id: int, worker_id: int):
    service_request = db.query(MOdelServiceRequest).filter(MOdelServiceRequest.id == service_request_id).first()

    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    worker=db.query(ModelWorkerRegister).filter(ModelWorkerRegister.id== worker_id).first()

    if not worker:
        raise HTTPException(status_code=404, detail="worker is not found")
    
    service_request.assigned_worker_id=worker.id
    service_request.status="Assigned"
    service_request.assigned_at = datetime.utcnow()

    db.commit()
    db.refresh(service_request)
    return service_request


# It will start the work
def start_work_request(db:Session, service_request_id:int):
    service_request=db.query(MOdelServiceRequest).filter(MOdelServiceRequest.id==service_request_id).first()

    if not service_request or service_request.status !="Assigned":
        raise HTTPException(status_code=404, detail="cannot start request")
    
    service_request.status="In Progress"
    service_request.started_at=datetime.utcnow()
    db.commit()
    db.refresh(service_request)
    return [service_request]


# It will complete the task
def complete_service_request(db: Session, service_request_id: int):
    service_request = db.query(MOdelServiceRequest).filter(
        MOdelServiceRequest.id == service_request_id
    ).first()

    if not service_request or service_request.status != "In Progress":
        raise HTTPException(status_code=400, detail="Cannot complete request")
    
    service_request.status = "Completed"
    service_request.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(service_request)
    return service_request


# Get all assigned requests for a worker
def get_requests_for_worker(db: Session, worker_id: int):
    return db.query(MOdelServiceRequest).filter(MOdelServiceRequest.assigned_worker_id == worker_id).all()


# Delete the service request by status
def delete_service_request(db: Session, service_request_id: int):
    service_request = db.query(MOdelServiceRequest).filter(
        MOdelServiceRequest.id == service_request_id
    ).first()

    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    if service_request.status in ["In Progress", "Assigned"]:
        raise HTTPException(status_code=400, detail="Cannot delete request that is in progress or assigned")
    
    db.delete(service_request)
    db.commit()
    return {"detail": "Service request deleted successfully"}


def get_all_assigned_service_requests(db: Session):
    return db.query(MOdelServiceRequest).filter(MOdelServiceRequest.status == "Assigned").all()


def get_all_completed_service_requests(db: Session):
    return db.query(MOdelServiceRequest).filter(MOdelServiceRequest.status == "Completed").all()


# =============================================================================
# BOREWELL RECOMMENDATION ENGINE
# Standards: IS 8034, IS 3961, Hazen-Williams, IEC 60034
# =============================================================================

# -- Internal constants (prefixed with _ so they don't pollute module scope) --

_FT_TO_M  = 0.3048
_GRAVITY  = 9.81
_DENSITY  = 1000
_KW_TO_HP = 1.341

_USAGE_PROFILES = {
    "home":        {"label": "Home / Villa",           "flow": 1000,  "duty": 0.40, "mat": "uPVC"},
    "apartment":   {"label": "Apartment / Commercial", "flow": 4000,  "duty": 0.60, "mat": "uPVC"},
    "agriculture": {"label": "Agriculture / Farm",     "flow": 9000,  "duty": 0.70, "mat": "GI"},
    "industrial":  {"label": "Industrial / Factory",   "flow": 15000, "duty": 0.85, "mat": "GI"},
}

# Pipe nominal IDs in mm — IS 4985 uPVC / IS 1239 GI
_PIPES = [
    {"name": '25mm (1")',   "id": 26.6},
    {"name": '32mm (1¼")', "id": 35.1},
    {"name": '40mm (1½")', "id": 40.9},
    {"name": '50mm (2")',   "id": 52.5},
    {"name": '63mm (2½")', "id": 63.0},
    {"name": '75mm (3")',   "id": 75.0},
]

# Cable table: (sq_mm, current_A, resistance_ohm_per_km) — IS 694 / IS 3961
_CABLES = [
    (1.5,  17,  13.30),
    (2.5,  23,  7.980),
    (4.0,  30,  4.950),
    (6.0,  38,  3.300),
    (10.0, 52,  1.910),
    (16.0, 70,  1.210),
    (25.0, 90,  0.780),
]

_STD_KW = [0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.0, 3.7,
           4.0,  5.5,  7.5,  11.0, 15.0, 18.5, 22.0, 30.0, 37.0, 45.0]

_MOTOR_EFF = {
    0.37: 0.68, 0.55: 0.71, 0.75: 0.74, 1.1:  0.77, 1.5:  0.79,
    2.2:  0.81, 3.0:  0.82, 3.7:  0.83, 4.0:  0.83, 5.5:  0.85,
    7.5:  0.86, 11.0: 0.87, 15.0: 0.88, 18.5: 0.88, 22.0: 0.89,
    30.0: 0.90, 37.0: 0.90, 45.0: 0.91,
}


def _safety_gap(bore_depth_ft: float) -> int:
    """Gap (ft) between motor bottom and bore bottom — your rule."""
    if bore_depth_ft <= 100: return 15
    if bore_depth_ft <= 200: return 20
    if bore_depth_ft <= 400: return 30
    return 40


def _hw_loss(flow_lph: float, id_mm: float, length_m: float, C: float) -> float:
    """Hazen-Williams friction loss in metres."""
    Q = flow_lph / (1000 * 3600)
    D = id_mm / 1000
    if not Q or not D:
        return 0.0
    return 10.67 * length_m * (Q ** 1.852) / ((C ** 1.852) * (D ** 4.871))


def _flow_velocity(flow_lph: float, id_mm: float) -> float:
    Q = flow_lph / (1000 * 3600)
    A = math.pi * ((id_mm / 1000) / 2) ** 2
    return Q / A


def _select_pipe(flow_lph: float, mat: str) -> dict:
    C = 140 if mat == "uPVC" else 120
    for p in _PIPES:
        v = _flow_velocity(flow_lph, p["id"])
        if v <= 2.0:
            return {**p, "velocity": round(v, 2), "C": C, "mat": mat, "warn": False}
    last = _PIPES[-1]
    return {**last, "velocity": round(_flow_velocity(flow_lph, last["id"]), 2),
            "C": C, "mat": mat, "warn": True}


def _pump_eff(flow_lph: float, tdh: float) -> float:
    Q = flow_lph / (1000 * 3600)
    if tdh <= 0:
        return 0.55
    Ns = 2900 * math.sqrt(Q) / (tdh ** 0.75)
    Ns = max(5, min(Ns, 120))
    eta = -0.000012 * Ns ** 2 + 0.004 * Ns + 0.42
    return max(0.35, min(eta, 0.74))


def _size_motor(flow_lph: float, tdh: float) -> dict:
    Q       = flow_lph / (1000 * 3600)
    eta_p   = _pump_eff(flow_lph, tdh)
    P_shaft = (_DENSITY * _GRAVITY * Q * tdh) / eta_p
    P_req   = (P_shaft / 0.81) * 1.15          # service factor 1.15

    rated_kw = next((k for k in _STD_KW if k * 1000 >= P_req), 45.0)
    eta_m    = _MOTOR_EFF.get(rated_kw, 0.83)
    P_input  = (P_shaft / 1000) / eta_m

    comm_hp = next(
        (h for h in [0.5, 1, 1.5, 2, 3, 5, 7.5, 10, 15, 20, 25, 30]
         if h >= rated_kw * _KW_TO_HP), 30
    )
    return {
        "rated_kw":   rated_kw,
        "comm_hp":    comm_hp,
        "eta_p":      round(eta_p, 3),
        "eta_m":      round(eta_m, 3),
        "P_shaft_kw": round(P_shaft / 1000, 3),
        "P_input_kw": round(P_input, 3),
    }


def _select_cable(motor_kw: float, pump_depth_m: float,
                  eta_m: float, voltage: int) -> dict:
    phases = 3 if voltage >= 380 else 1
    if phases == 3:
        flc = (motor_kw * 1000) / (math.sqrt(3) * voltage * 0.82 * eta_m)
    else:
        flc = (motor_kw * 1000) / (voltage * 0.85 * eta_m)

    cable_run_m = pump_depth_m + 5

    for sq_mm, i_cap, r_km in _CABLES:
        if i_cap < flc / 1.05:
            continue
        R = (r_km / 1000) * cable_run_m
        vd_pct = ((math.sqrt(3) * flc * R / voltage) * 100 if phases == 3
                  else (2 * flc * R / voltage) * 100)
        if vd_pct <= 5.0:
            return {"sq_mm": sq_mm, "flc": round(flc, 2),
                    "vd_pct": round(vd_pct, 2), "warn": False}

    sq_mm, _, r_km = _CABLES[-1]
    R = (r_km / 1000) * cable_run_m
    vd_pct = ((math.sqrt(3) * flc * R / voltage) * 100 if phases == 3
              else (2 * flc * R / voltage) * 100)
    return {"sq_mm": sq_mm, "flc": round(flc, 2),
            "vd_pct": round(vd_pct, 2), "warn": True}


def _select_starter(kw: float) -> str:
    if kw <= 1.1:  return "DOL Starter with overload relay"
    if kw <= 5.5:  return "Star-Delta (Y/Δ) Starter"
    if kw <= 15:   return "Electronic Soft Starter"
    return "Variable Frequency Drive (VFD)"


def _select_pump_type(bore_dia_inch: float, tdh: float) -> dict:
    if bore_dia_inch <= 4:
        if tdh > 200:
            return {"type": "4\" High-Head Multi-Stage Submersible",
                    "note": "15–25 stages, radial flow"}
        return {"type": "4\" Multi-Stage Submersible",
                "note": "6–14 stages, radial flow"}
    if bore_dia_inch <= 6:
        return {"type": "6\" Multi-Stage Submersible",
                "note": "Mixed/radial flow, better efficiency"}
    return {"type": "8\"+ Submersible / Vertical Turbine Pump",
            "note": "High capacity bore"}


# =============================================================================

def create_borewell_details(borewell):
    try:
        # -------- INPUT --------
        bore_depth = float(borewell.bore_depth)
        water_level = float(borewell.water_level)
        bore_dia = float(borewell.casing_diameter)
        floors = int(borewell.floors_supply)

        voltage = 230 if borewell.electricity_supply == 1 else 415

        usage_map = {
            1: "home",
            2: "apartment",
            3: "agriculture",
            4: "industrial"
        }
        usage = usage_map.get(borewell.usage_type)

        if not usage:
            raise Exception("Invalid usage")

    except Exception as e:
        raise Exception(f"Invalid input: {str(e)}")

    # -------- CONSTANTS --------
    FT_TO_M = 0.3048

    # -------- WATER LEVEL --------
    static_m = water_level * FT_TO_M

    if bore_depth <= 300:
        drawdown_factor = 0.3
    elif bore_depth <= 800:
        drawdown_factor = 0.4
    else:
        drawdown_factor = 0.5

    dynamic_m = static_m * (1 + drawdown_factor)

    # -------- DELIVERY --------
    delivery_m = (floors * 3) + 5

    # -------- FRICTION LOSS --------
    if bore_depth <= 300:
        friction_loss = 5
    elif bore_depth <= 800:
        friction_loss = 10
    else:
        friction_loss = 15

    # -------- TOTAL HEAD --------
    tdh = dynamic_m + delivery_m + friction_loss

    # -------- MOTOR HP --------
    if tdh <= 50:
        motor_hp = 1
    elif tdh <= 80:
        motor_hp = 1.5
    elif tdh <= 120:
        motor_hp = 2
    elif tdh <= 180:
        motor_hp = 3
    elif tdh <= 250:
        motor_hp = 5
    elif tdh <= 350:
        motor_hp = 7.5
    else:
        motor_hp = 10

    # -------- PUMP TYPE --------
    if bore_dia <= 4:
        pump_type = "4-inch submersible (radial flow)"
    elif bore_dia <= 6:
        pump_type = "6-inch submersible (mixed flow)"
    else:
        pump_type = "8-inch submersible (high discharge)"

    # -------- PIPE SIZE --------
    if motor_hp <= 1:
        pipe = "1–1.25 inch (25–32mm)"
    elif motor_hp <= 2:
        pipe = "1.25 inch (32mm)"
    elif motor_hp <= 5:
        pipe = "1.5 inch (40mm)"
    else:
        pipe = "2 inch (50mm)"

    # Depth correction
    if bore_depth > 800 and motor_hp >= 5:
        pipe = "2 inch (50mm) – recommended for deep bore"
    elif bore_depth > 500 and motor_hp >= 3:
        pipe = "1.5–2 inch (40–50mm)"

    # Usage boost
    if usage in ["agriculture", "industrial"] and motor_hp >= 5:
        pipe = "2 inch (50mm) – high discharge usage"

    pipe_length = bore_depth - 25

    # -------- CABLE SIZE --------
    if bore_depth <= 200:
        cable = 1.5 if motor_hp <= 1 else 2.5
    elif bore_depth <= 400:
        cable = 2.5 if motor_hp <= 2 else 4
    elif bore_depth <= 800:
        cable = 4 if motor_hp <= 5 else 6
    else:
        cable = 6 if motor_hp <= 7.5 else 10

    cable_length = bore_depth + 20

    # -------- CURRENT --------
    if voltage == 230:
        current = round(motor_hp * 5, 1)
    else:
        current = round(motor_hp * 2, 1)

    # -------- RUN TIME --------
    if water_level <= 50:
        hours = 5
    elif water_level <= 100:
        hours = 4
    elif water_level <= 200:
        hours = 3
    else:
        hours = 2

    # -------- POWER COST CALCULATION --------
    def calculate_monthly_cost(hp, hours_per_day, voltage):
        power_kw = hp * 0.75
        units_per_day = power_kw * hours_per_day
        monthly_units = units_per_day * 30

        # Approx electricity rate
        if voltage == 230:
            rate = 7   # domestic
        else:
            rate = 6   # 3-phase

        monthly_cost = monthly_units * rate

        return round(monthly_units, 1), round(monthly_cost, 0)

    monthly_units, monthly_cost = calculate_monthly_cost(motor_hp, hours, voltage)

    # -------- FINAL OUTPUT --------
    return {
        "Total Dynamic Head (m)": round(tdh, 2),

        "Recommended Pump Set": f"{motor_hp} HP, {pump_type}",

        "Pipe Size": pipe,
        "Pipe Length": f"{int(pipe_length)} ft",

        "Cable Size": f"{cable} sq mm",
        "Cable Length": f"{int(cable_length)} ft",

        "Recommended Running Time": f"{hours} hours/day",

        "Motor Current": f"{current} A",
        "Voltage": f"{voltage} V",

        "Estimated Power Consumption": f"{monthly_units} units/month",
        "Estimated Monthly Cost": f"₹{monthly_cost}",

        "Note": "Includes safety margin for seasonal water level drop"
    }