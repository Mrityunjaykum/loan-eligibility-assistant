def check_eligibility(applicant_data: dict):
    age = applicant_data.get("age")
    salary = applicant_data.get("salary")
    loan_amount = applicant_data.get("loanAmount")
    credit_score = applicant_data.get("creditScore")
    
    reasons = []
    if age < 21: reasons.append("Age must be >= 21")
    if salary < 30000: reasons.append("Salary must be >= 30,000")
    if credit_score < 700: reasons.append("Credit score must be >= 700")
    if loan_amount > (10 * salary): reasons.append(f"Loan amount exceeds 10x salary (Max: {10 * salary})")
        
    if not reasons:
        return {"eligible": True, "reason": "All criteria satisfied."}
    return {"eligible": False, "reason": "; ".join(reasons)}