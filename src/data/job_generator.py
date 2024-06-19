import pandas as pd
import random
import math
from collections import defaultdict

# Data sample untuk pengisian dataset
job_titles = [
    "Data Scientist", "Data Analyst", "Business Intelligence Analyst", "Data Engineer", "Research Scientist", 
    "Big Data Specialist", "Data Mining Engineer", "Machine Learning Engineer", "AI Research Scientist", 
    "Deep Learning Engineer", "NLP Engineer (Natural Language Processing)", "Computer Vision Engineer", 
    "Robotics Engineer", "Reinforcement Learning Specialist", "Web Developer", "Front-end Developer", 
    "Back-end Developer", "Full-stack Developer", "UI/UX Developer", "JavaScript Developer", 
    "Web Application Developer", "Technical Project Manager", "IT Project Manager", "Agile Project Manager", 
    "Product Manager", "Program Manager", "Scrum Master", "Graphic Designer", "UI Designer", 
    "UX Designer", "Motion Graphics Designer", "Brand Designer", "Interaction Designer"
]

ratings = [round(random.uniform(2.5, 5.0), 1) for _ in range(1000)]
company_names = [
    "PT Telkom Indonesia", "GoJek", "Tokopedia", "Bukalapak", "Traveloka",
    "Bank Central Asia (BCA)", "Bank Rakyat Indonesia (BRI)", "Bank Mandiri",
    "Bank Negara Indonesia (BNI)", "Pertamina", "PLN (Perusahaan Listrik Negara)",
    "Garuda Indonesia", "Astra International", "Indofood", "Unilever Indonesia",
    "Sampoerna", "Kalbe Farma", "XL Axiata", "Indosat Ooredoo",
    "Telekomunikasi Selular (Telkomsel)", "Blue Bird Group", "Matahari Department Store",
    "Lippo Group", "Ciputra Development", "Djarum", "Gudang Garam", "Sinar Mas Group",
    "Indomaret", "Alfamart", "Bumi Resources"
]
company_to_industry = {
    "PT Telkom Indonesia": "Telecommunications",
    "GoJek": "E-commerce",
    "Tokopedia": "E-commerce",
    "Bukalapak": "E-commerce",
    "Traveloka": "E-commerce",
    "Bank Central Asia (BCA)": "Banking",
    "Bank Rakyat Indonesia (BRI)": "Banking",
    "Bank Mandiri": "Banking",
    "Bank Negara Indonesia (BNI)": "Banking",
    "Pertamina": "Oil and Gas",
    "PLN (Perusahaan Listrik Negara)": "Energy",
    "Garuda Indonesia": "Airlines",
    "Astra International": "Automotive",
    "Indofood": "Food and Beverage",
    "Unilever Indonesia": "Consumer Goods",
    "Sampoerna": "Tobacco",
    "Kalbe Farma": "Pharmaceuticals",
    "XL Axiata": "Telecommunications",
    "Indosat Ooredoo": "Telecommunications",
    "Telekomunikasi Selular (Telkomsel)": "Telecommunications",
    "Blue Bird Group": "Transportation",
    "Matahari Department Store": "Retail",
    "Lippo Group": "Conglomerate",
    "Ciputra Development": "Real Estate",
    "Djarum": "Tobacco",
    "Gudang Garam": "Tobacco",
    "Sinar Mas Group": "Conglomerate",
    "Indomaret": "Retail",
    "Alfamart": "Retail",
    "Bumi Resources": "Mining"
}

sectors = ["Technology", "Finance", "Healthcare", "Energy", "Retail", "Transportation", "Telecommunications", "Consumer Goods", "Conglomerate"]
industry_to_sector = {
    "Information Technology": "Technology",
    "Software": "Technology",
    "E-commerce": "Technology",
    "Telecommunications": "Telecommunications",
    "Financial Services": "Finance",
    "Banking": "Finance",
    "Oil and Gas": "Energy",
    "Energy": "Energy",
    "Airlines": "Transportation",
    "Automotive": "Transportation",
    "Food and Beverage": "Consumer Goods",
    "Consumer Goods": "Consumer Goods",
    "Pharmaceuticals": "Healthcare",
    "Transportation": "Transportation",
    "Retail": "Retail",
    "Real Estate": "Real Estate",
    "Tobacco": "Consumer Goods",
    "Conglomerate": "Conglomerate",
    "Mining": "Energy"
}

locations = ["Remote","Ambon", "Balikpapan", "Banda Aceh", "Bandar Lampung", "Bandung", "Banjar", "Banjarbaru", "Banjarmasin", "Batam", "Batu", "Bau-Bau", "Bekasi", "Bengkulu", "Binjai", "Bitung", "Blitar", "Bogor", "Bontang", "Bukittinggi", "Cilegon", "Cimahi", "Cirebon", "Denpasar", "Depok", "Dumai", "Gorontalo", "Gunungsitoli", "Jakarta", "Jambi", "Jayapura", "Kediri", "Kendari", "Kotamobagu", "Kupang", "Langsa", "Lhokseumawe", "Lubuklinggau", "Madiun", "Magelang", "Makassar", "Malang", "Manado", "Mataram", "Medan", "Metro", "Mojokerto", "Padang", "Padang Panjang", "Padang Sidempuan", "Pagar Alam", "Palangka Raya", "Palembang", "Palopo", "Palu", "Pangkal Pinang", "Parepare", "Pariaman", "Pasuruan", "Payakumbuh", "Pekalongan", "Pekanbaru", "Pematang Siantar", "Pontianak", "Prabumulih", "Probolinggo", "Sabang", "Salatiga", "Samarinda", "Sawah Lunto", "Semarang", "Serang", "Singkawang", "Solok", "Sorong", "Subulussalam", "Sukabumi", "Sungai Penuh", "Surabaya", "Surakarta", "Tangerang", "Tangerang Selatan", "Tanjungbalai", "Tanjungpinang", "Tarakan", "Tasikmalaya", "Tebing Tinggi", "Tegal", "Ternate", "Tidore Kepulauan", "Tomohon", "Tual", "Yogyakarta"]
headquarters = ["Jakarta", "Surabaya", "Bandung", "Medan", "Padang", "Yogyakarta"]
sizes = ["1001 to 5000 employees", "5001 to 10000 employees", "10001+ employees"]
founded = [1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009, 2010, 2011, 2012, 2013]
types_of_ownership = ["Company - Private","Company - Public","Company - Non-profit", "Company - Government","Company - Joint Venture","Company - Partnership","Company - Sole Proprietorship","Company - Cooperative","Company - Subsidiary","Company - Holding","Company - Limited Liability Company (LLC)","Company - Corporation (C Corp)","Company - S Corporation (S Corp)","Company - Professional Corporation (PC)","Company - Limited Partnership (LP)","Company - Limited Liability Partnership (LLP)"]
competitors = ["None", "Undefined"]
average_revenues = [round(random.uniform(15, 100000), 1) for _ in range(1000)]

# Job description templates
jd_templates = {
    "Data Scientist": "We are looking for a Data Scientist to join our team. Requirements: Experience in {skills}. Responsibilities: {responsibilities}.",
    "Data Analyst": "Seeking a Data Analyst proficient in {skills}. Responsibilities include {responsibilities}.",
    "Business Intelligence Analyst": "We need a Business Intelligence Analyst with skills in {skills}. Main tasks: {responsibilities}.",
    "Data Engineer": "Hiring a Data Engineer experienced with {skills}. You will be responsible for {responsibilities}.",
    "Research Scientist": "Join us as a Research Scientist. Required skills: {skills}. Duties: {responsibilities}.",
    "Big Data Specialist": "We are looking for a Big Data Specialist skilled in {skills}. Responsibilities include {responsibilities}.",
    "Data Mining Engineer": "Seeking a Data Mining Engineer proficient in {skills}. Responsibilities include {responsibilities}.",
    "Machine Learning Engineer": "Join our team as a Machine Learning Engineer. Skills required: {skills}. Responsibilities: {responsibilities}.",
    "AI Research Scientist": "We need an AI Research Scientist with skills in {skills}. Main tasks: {responsibilities}.",
    "Deep Learning Engineer": "Hiring a Deep Learning Engineer experienced with {skills}. You will be responsible for {responsibilities}.",
    "NLP Engineer (Natural Language Processing)": "Join us as an NLP Engineer. Required skills: {skills}. Duties: {responsibilities}.",
    "Computer Vision Engineer": "We are looking for a Computer Vision Engineer skilled in {skills}. Responsibilities include {responsibilities}.",
    "Robotics Engineer": "Seeking a Robotics Engineer proficient in {skills}. Responsibilities include {responsibilities}.",
    "Reinforcement Learning Specialist": "Join our team as a Reinforcement Learning Specialist. Skills required: {skills}. Responsibilities: {responsibilities}.",
    "Web Developer": "We need a Web Developer proficient in {skills}. Responsibilities: {responsibilities}.",
    "Front-end Developer": "Seeking a Front-end Developer with skills in {skills}. Responsibilities: {responsibilities}.",
    "Back-end Developer": "Hiring a Back-end Developer experienced with {skills}. Responsibilities: {responsibilities}.",
    "Full-stack Developer": "We need a Full-stack Developer with skills in {skills}. Main tasks: {responsibilities}.",
    "UI/UX Developer": "Join us as a UI/UX Developer. Required skills: {skills}. Duties: {responsibilities}.",
    "JavaScript Developer": "Hiring a JavaScript Developer proficient in {skills}. Responsibilities: {responsibilities}.",
    "Web Application Developer": "We are looking for a Web Application Developer skilled in {skills}. Responsibilities include {responsibilities}.",
    "Technical Project Manager": "Seeking a Technical Project Manager proficient in {skills}. Responsibilities include {responsibilities}.",
    "IT Project Manager": "Join our team as an IT Project Manager. Skills required: {skills}. Responsibilities: {responsibilities}.",
    "Agile Project Manager": "We need an Agile Project Manager with skills in {skills}. Main tasks: {responsibilities}.",
    "Product Manager": "Hiring a Product Manager experienced with {skills}. You will be responsible for {responsibilities}.",
    "Program Manager": "Join us as a Program Manager. Required skills: {skills}. Duties: {responsibilities}.",
    "Scrum Master": "We are looking for a Scrum Master skilled in {skills}. Responsibilities include {responsibilities}.",
    "Graphic Designer": "Seeking a Graphic Designer proficient in {skills}. Responsibilities: {responsibilities}.",
    "UI Designer": "Hiring a UI Designer experienced with {skills}. Responsibilities: {responsibilities}.",
    "UX Designer": "We need a UX Designer with skills in {skills}. Main tasks: {responsibilities}.",
    "Motion Graphics Designer": "Join us as a Motion Graphics Designer. Required skills: {skills}. Duties: {responsibilities}.",
    "Brand Designer": "Hiring a Brand Designer proficient in {skills}. Responsibilities: {responsibilities}.",
    "Interaction Designer": "We are looking for an Interaction Designer skilled in {skills}. Responsibilities include {responsibilities}."
}

# Skills and responsibilities dictionaries
skills_dict = {
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Data Analysis", "R"],
    "Data Analyst": ["Excel", "SQL", "Data Visualization", "Power BI", "Tableau"],
    "Business Intelligence Analyst": ["BI Tools", "SQL", "Data Modeling", "Analytics", "Dashboarding"],
    "Data Engineer": ["ETL", "Python", "SQL", "Big Data", "Hadoop"],
    "Research Scientist": ["Python", "R", "Statistics", "Data Analysis", "Machine Learning"],
    "Big Data Specialist": ["Hadoop", "Spark", "Python", "NoSQL", "Big Data"],
    "Data Mining Engineer": ["Data Mining", "Python", "R", "SQL", "Algorithms"],
    "Machine Learning Engineer": ["Python", "TensorFlow", "Deep Learning", "Scikit-Learn", "NLP"],
    "AI Research Scientist": ["AI", "Python", "Machine Learning", "Algorithms", "Research"],
    "Deep Learning Engineer": ["Deep Learning", "Python", "TensorFlow", "Keras", "Neural Networks"],
    "NLP Engineer (Natural Language Processing)": ["NLP", "Python", "Text Mining", "SpaCy", "NLTK"],
    "Computer Vision Engineer": ["Computer Vision", "Python", "OpenCV", "Deep Learning", "Image Processing"],
    "Robotics Engineer": ["Robotics", "Python", "C++", "ROS", "Control Systems"],
    "Reinforcement Learning Specialist": ["Reinforcement Learning", "Python", "TensorFlow", "Algorithms", "Machine Learning"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "Front-end Developer": ["HTML", "CSS", "JavaScript", "React", "Vue.js"],
    "Back-end Developer": ["Node.js", "Java", "Python", "SQL", "APIs"],
    "Full-stack Developer": ["HTML", "CSS", "JavaScript", "Node.js", "React"],
    "UI/UX Developer": ["UI Design", "UX Research", "Prototyping", "Adobe XD", "Sketch"],
    "JavaScript Developer": ["JavaScript", "React", "Node.js", "Vue.js", "Angular"],
    "Web Application Developer": ["Web Development", "JavaScript", "APIs", "HTML", "CSS"],
    "Technical Project Manager": ["Project Management", "Agile", "Scrum", "Technical Background", "Leadership"],
    "IT Project Manager": ["IT Project Management", "Agile", "Scrum", "Technical Background", "Leadership"],
    "Agile Project Manager": ["Agile", "Scrum", "Project Management", "Leadership", "Communication"],
    "Product Manager": ["Product Management", "Agile", "Scrum", "Product Development", "Leadership"],
    "Program Manager": ["Program Management", "Agile", "Scrum", "Leadership", "Communication"],"Scrum Master": ["Scrum", "Agile", "Project Management", "Facilitation", "Team Collaboration"],
    "Graphic Designer": ["Adobe Photoshop", "Illustrator", "InDesign", "Creativity", "Graphic Design"],
    "UI Designer": ["UI Design", "Sketch", "Figma", "Adobe XD", "Prototyping"],
    "UX Designer": ["UX Research", "Wireframing", "Prototyping", "Adobe XD", "Sketch"],
    "Motion Graphics Designer": ["After Effects", "Cinema 4D", "Animation", "Motion Graphics", "Creativity"],
    "Brand Designer": ["Brand Strategy", "Graphic Design", "Adobe Creative Suite", "Creativity", "Visual Design"],
    "Interaction Designer": ["Interaction Design", "Prototyping", "User Testing", "UI Design", "Adobe XD"]
}

responsibilities_dict = {
    "Data Scientist": ["Analyze data to drive insights", "Develop predictive models", "Work with large datasets", "Collaborate with cross-functional teams", "Communicate findings to stakeholders"],
    "Data Analyst": ["Analyze business data", "Create reports and dashboards", "Work with SQL and Excel", "Identify trends and patterns", "Support data-driven decision making"],
    "Business Intelligence Analyst": ["Develop BI solutions", "Create and maintain dashboards", "Work with business stakeholders", "Analyze data trends", "Provide actionable insights"],
    "Data Engineer": ["Build and maintain data pipelines", "Develop ETL processes", "Work with big data technologies", "Ensure data quality and integrity", "Collaborate with data scientists"],
    "Research Scientist": ["Conduct research and experiments", "Develop new methodologies", "Analyze experimental data", "Publish research findings", "Collaborate with other scientists"],
    "Big Data Specialist": ["Manage and analyze large datasets", "Develop big data solutions", "Work with Hadoop and Spark", "Ensure data scalability", "Collaborate with data engineers"],
    "Data Mining Engineer": ["Develop data mining models", "Analyze large datasets", "Work with data scientists", "Optimize algorithms", "Provide actionable insights"],
    "Machine Learning Engineer": ["Develop machine learning models", "Work with TensorFlow and PyTorch", "Collaborate with data scientists", "Optimize ML algorithms", "Deploy ML solutions"],
    "AI Research Scientist": ["Conduct AI research", "Develop new AI algorithms", "Analyze experimental results", "Publish research papers", "Collaborate with other researchers"],
    "Deep Learning Engineer": ["Develop deep learning models", "Work with TensorFlow and Keras", "Optimize neural networks", "Collaborate with data scientists", "Deploy DL solutions"],
    "NLP Engineer (Natural Language Processing)": ["Develop NLP models", "Work with text data", "Use NLP libraries", "Collaborate with linguists", "Deploy NLP solutions"],
    "Computer Vision Engineer": ["Develop computer vision models", "Work with image data", "Use OpenCV and TensorFlow", "Optimize image processing algorithms", "Collaborate with data scientists"],
    "Robotics Engineer": ["Develop robotics solutions", "Work with control systems", "Program robots", "Test and optimize robotics algorithms", "Collaborate with other engineers"],
    "Reinforcement Learning Specialist": ["Develop RL models", "Work with TensorFlow and PyTorch", "Optimize RL algorithms", "Conduct experiments", "Collaborate with data scientists"],
    "Web Developer": ["Develop and maintain websites", "Work with HTML, CSS, and JavaScript", "Ensure website performance", "Collaborate with designers", "Optimize web applications"],
    "Front-end Developer": ["Develop user interfaces", "Work with HTML, CSS, and JavaScript", "Ensure responsive design", "Collaborate with back-end developers", "Optimize front-end performance"],
    "Back-end Developer": ["Develop server-side logic", "Work with databases", "Ensure application performance", "Collaborate with front-end developers", "Optimize server-side code"],
    "Full-stack Developer": ["Develop both front-end and back-end", "Work with HTML, CSS, JavaScript, and server-side languages", "Ensure full-stack performance", "Collaborate with designers and developers", "Optimize full-stack applications"],
    "UI/UX Developer": ["Design user interfaces and experiences", "Work with design tools", "Conduct user research", "Collaborate with developers", "Create prototypes"],
    "JavaScript Developer": ["Develop applications using JavaScript", "Work with frameworks like React and Node.js", "Ensure code quality", "Collaborate with other developers", "Optimize JavaScript performance"],
    "Web Application Developer": ["Develop web applications", "Work with JavaScript and APIs", "Ensure application security", "Collaborate with designers", "Optimize web application performance"],
    "Technical Project Manager": ["Manage technical projects", "Work with cross-functional teams", "Ensure project delivery", "Manage project timelines", "Communicate with stakeholders"],
    "IT Project Manager": ["Manage IT projects", "Work with IT teams", "Ensure project success", "Manage project budgets", "Communicate with stakeholders"],
    "Agile Project Manager": ["Manage agile projects", "Facilitate agile processes", "Ensure project delivery", "Collaborate with agile teams", "Communicate with stakeholders"],
    "Product Manager": ["Manage product lifecycle", "Work with cross-functional teams", "Define product vision", "Ensure product success", "Communicate with stakeholders"],
    "Program Manager": ["Manage programs", "Coordinate multiple projects", "Ensure program delivery", "Manage program budgets", "Communicate with stakeholders"],
    "Scrum Master": ["Facilitate scrum processes", "Support agile teams", "Ensure team productivity", "Remove obstacles", "Communicate with stakeholders"],
    "Graphic Designer": ["Create visual designs", "Work with design tools", "Collaborate with marketing teams", "Ensure design quality", "Develop branding materials"],
    "UI Designer": ["Design user interfaces", "Work with design tools", "Collaborate with developers", "Ensure design consistency", "Create prototypes"],
    "UX Designer": ["Conduct user research", "Design user experiences", "Collaborate with developers", "Ensure usability", "Create wireframes and prototypes"],
    "Motion Graphics Designer": ["Create motion graphics", "Work with animation tools", "Collaborate with video production teams", "Ensure animation quality", "Develop visual content"],
    "Brand Designer": ["Develop branding materials", "Work with design tools", "Collaborate with marketing teams", "Ensure brand consistency", "Create visual identities"],
    "Interaction Designer": ["Design interactive experiences", "Work with design tools", "Collaborate with developers", "Ensure interaction quality", "Create prototypes"]
}

def create_sector_to_companies_mapping(company_to_industry, industry_to_sector):
    sector_to_companies = defaultdict(list)
    for company, industry in company_to_industry.items():
        sector = industry_to_sector[industry]
        sector_to_companies[sector].append(company)
    return sector_to_companies

sector_to_companies = create_sector_to_companies_mapping(company_to_industry, industry_to_sector)

# Assign a single revenue, size, founded year, type of ownership, and headquarters to each company
company_to_revenue = {company: math.ceil(revenue) for company, revenue in zip(company_names, average_revenues)}
company_to_size = {company: random.choice(sizes) for company in company_names}
company_to_founded = {company: random.choice(founded) for company in company_names}
company_to_ownership = {company: random.choice(types_of_ownership) for company in company_names}
company_to_headquarters = {company: random.choice(headquarters) for company in company_names}

# Generate dataset
def generate_processed_jd(job_title):
    skills = random.sample(skills_dict[job_title], 3)
    responsibilities = random.sample(responsibilities_dict[job_title], 3)
    return jd_templates[job_title].format(skills=", ".join(skills), responsibilities=", ".join(responsibilities))

data = []
for _ in range(1000):
    job_title = random.choice(job_titles)
    company = random.choice(list(company_to_industry.keys()))
    industry = company_to_industry[company]
    sector = industry_to_sector[industry]
    competitors_in_sector = sector_to_companies[sector]
    competitors = random.sample([comp for comp in competitors_in_sector if comp != company], min(3, len(competitors_in_sector)-1))
    average_revenue = math.ceil(company_to_revenue[company])
    average_salary = math.ceil(random.uniform(0.05, 0.09) * average_revenue)
    data.append([
        job_title,
        random.choice(ratings),
        company,
        random.choice(locations),
        company_to_headquarters[company],
        company_to_size[company],
        company_to_founded[company],
        company_to_ownership[company],
        industry,
        sector,
        ", ".join(competitors),
        average_salary,
        average_revenue,
        generate_processed_jd(job_title)
    ])

# Convert to DataFrame
columns = [
    "Job Title", "Rating", "Company Name", "Location", "Headquarters", "Size", "Founded", 
    "Type of ownership", "Industry", "Sector", "Competitors", "Average Salary", "Average Revenue", "Processed_JD"
]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv("D:/ML_Projects/Job_Reccomendation_System/src/data/jd_structured_data.csv", index=False)


