# 🧹 Data Cleaning Project – `aus_ccx_21.csv`

## 📌 Project Overview
This project demonstrates a **complete data cleaning pipeline** using **Pandas**.  
The dataset `aus_ccx_21.csv` contains employee records with issues like:  
- Leading/trailing spaces  
- Invalid or missing emails  
- Mixed date formats  
- Salaries and sales with text/units (`USD`, `$`)  
- Duplicate records  
- Missing values in remarks and time fields  

The goal of this project is to **clean, validate, and prepare the dataset** for further analysis.

---

## ⚙️ Cleaning Steps
The cleaning pipeline performs the following steps:

1. **String Cleaning**
   - Removed leading/trailing spaces across all text columns  
   - Standardized remarks (removed double spaces, filled missing with `"unknown"`)  

2. **Email Validation**
   - Converted emails to lowercase  
   - Validated format using regex  
   - Replaced invalid emails with `"unknown@no_mail.com"`  

3. **Date Cleaning**
   - Handled `"Not Available"` in `join_date`  
   - Converted to datetime with `dayfirst=True`  

4. **Numeric Columns**
   - Cleaned `salary` and `sales` by removing `$`, `USD`  
   - Converted to numeric  
   - Cleaned `time_productive` by removing `"hrs"`  

5. **Missing Values**
   - Filled invalid emails with placeholder  
   - Filled missing remarks with `"unknown"`  
   - Filled missing salary with a random value in range `43,571 – 60,809`  

6. **Duplicate Handling**
   - Dropped duplicates based on `first_name`, `last_name`, `email`  

7. **Feature Engineering**
   - Added `increment_percentage` based on sales brackets  
   - Computed `Updated_salary` after increment  
   - Added `termination_flag` for employees meeting risk criteria  
   - Computed `experience` in years + days  
   - Flagged employees in **promotion pipeline**  

---

## 📊 Key Outputs
- **Highest recorded sales**  
- **Central average, median, mode of sales**  
- **Promotion eligibility**  
- **Termination flags**  
