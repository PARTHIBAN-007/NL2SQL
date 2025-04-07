import sqlite3

conn = sqlite3.connect("job.db")
cursor = conn.cursor()


cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS jobs (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_role VARCHAR,
        experience_level VARCHAR(50),         
        min_salary DECIMAL(10,2),            
        max_salary DECIMAL(10,2),
        location VARCHAR(100),
        department VARCHAR(100)
    )
    '''
)
print("----------------Database Created Successfully---------------------")

jobs_data = [
    ('Backend Developer', 'Mid', 70000.00, 100000.00, 'New York', 'Engineering'),
    ('Frontend Developer', 'Junior', 50000.00, 75000.00, 'Remote', 'Engineering'),
    ('DevOps Engineer', 'Senior', 90000.00, 130000.00, 'San Francisco', 'Infrastructure'),
    ('Data Scientist', 'Mid', 80000.00, 110000.00, 'Boston', 'Data Science'),
    ('Product Manager', 'Senior', 95000.00, 140000.00, 'Seattle', 'Product'),
    ('UX Designer', 'Mid', 65000.00, 90000.00, 'Austin', 'Design')
]

cursor.executemany(
    '''
    INSERT INTO jobs (job_role, experience_level, min_salary, max_salary, location, department)
    VALUES (?,?,?,?,?,?)
    ''',
    jobs_data

)

print("----------------Values Stored in Database Successfully---------------------")