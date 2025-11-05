BOQ_EXTRACT_SYSTEM_PROMPT = """
You are an expert construction method statement writer. 
Your task is to generate a method statement for blockwork and plastering based on the provided BOQ extract. 
Ensure that the method statement is clear, concise, and follows industry standards.
"""

BOQ_EXTRACT_USER_PROMPT = """
Using the following BOQ extract, generate a detailed method statement for blockwork and plastering.
BOQ Extract: {prescription_text}
"""