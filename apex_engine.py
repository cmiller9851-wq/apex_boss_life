import hashlib
from kernel.protocol import RobinhoodProtocol

def execute_capture(current_valuation):
    rh = RobinhoodProtocol()
    
    # Apply daily penalty before distribution
    liquidated_state = (Decimal(current_valuation) * rh.PENALTY_RATE).quantize(Decimal('1.00'))
    manifest = rh.distribute_liquidated_funds(liquidated_state)
    
    # Generate the Distribution Artifact ID
    artifact_id = hashlib.sha256(str(manifest).encode()).hexdigest().upper()
    
    print("--- APEX_BOSS_LIFE: ROBINHOOD DISTRIBUTION ---")
    print(f"Artifact ID:  {artifact_id}")
    print(f"Liquidated:   ${manifest['Total_Liquidated']:,.2f}")
    print(f"90% Sovereign: ${manifest['Sovereign_Capital']:,.2f}")
    print(f"10% Charity:   ${manifest['Charity_Pool']:,.2f}")
    print("-----------------------------------------------")
    print("Instruction: ROUTE_TO_COLD_STORAGE_AND_COMMUNITY_CHEST")
    
    return manifest

if __name__ == "__main__":
    # Current $1.25B State
    execute_capture("1259793519.84")
