
import os

# Path to the CSV file
file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")
    
# Reading the file and handling potential format issues
try:
    with open(file_path, 'r') as file:
        lines = file.readlines()
except Exception as e:
    raise IOError(f"Error reading the file: {e}")

# Variables to store team scores and individual results
team_scores = []
individual_results = []

# Booleans to detect sections
in_team_scores = False
in_individual_results = False

# For loop to capture data sections
for line in lines:
    line = line.strip()

    if line.startswith("Place,Team,Score"):
        in_team_scores = True
        in_individual_results = False
        continue
    elif line.startswith("Place,Grade,Name,Athlete Link,Time,Team,Team Link,Profile Pic"):
        in_team_scores = False
        in_individual_results = True
        continue
    elif not line:  # Ignores the empty lines
        continue

    data = line.split(',')

    # Validate CSV structure for teams and individuals and limit to top 3 results
    if in_team_scores and len(team_scores) < 3:
        if len(data) >= 3 and all(data[:3]):
            team_scores.append(data[:3])
        else:
            print(f"Warning: Incorrect or incomplete team score data: {line}")
    elif in_individual_results and len(individual_results) < 3:
        if len(data) >= 8 and all(data[:8]):
            individual_results.append(data[:8])
        else:
            print(f"Warning: Incorrect or incomplete individual result data: {line}")

# Report any issues if less than 3 entries are found
if len(team_scores) < 3:
    print("Warning: Less than 3 valid team scores found.")
if len(individual_results) < 3:
    print("Warning: Less than 3 valid individual results found.")

# HTML content to be constructed directly
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="css/reset.css"> 
    <link rel="stylesheet" href="css/style.css">
    <title>Client Project - Results</title>
    <!-- <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        div.athlete {
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
        }
    </style> -->
</head>
<body>
    <header id="main-header">
        <nav id="main-nav">
            <ul>
                <li><a href="pages/mens.html">Mens</a></li>
                <li><a href="pages/womens.html">Womens</a></li>
                <li><a href="pages/grade9.html">Grade 9</a></li>
                <li><a href="pages/grade10.html">Grade 10</a></li>
                <li><a href="pages/grade11.html">Grade 11</a></li>
                <li><a href="pages/grade12.html">Grade 12</a></li>
            </ul>
        </nav>
        <h1>Event Summary</h1>
    </header>
    <main id="content">
        <section id="event-title">
            <h2>SEC Jamboree #1 Womens 5000 Meters Junior Varsity</h2>
        </section>
        <section id="team-scores">
            <h2>Team Scores</h2>
            <table>
                <thead>
                    <tr>
                        <th>Place</th>
                        <th>Team</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
"""

# Adds top 3 team scores to the HTML content
for score in team_scores:
    if len(score) >= 3:
        html_content += f"""
                    <tr>
                        <td>{score[0]}</td>
                        <td>{score[1]}</td>
                        <td>{score[2]}</td>
                    </tr>
        """

# Closes the team scores table tag
html_content += """
                </tbody>
            </table>
        </section>
        <section id="individual-results">
            <h2>Top 3 Results</h2>
"""

# Creates the HTML content for top 3 individual athletes
for result in individual_results:
    if len(result) >= 7:  # Making sure all required data is present!!
        athlete_link = result[3]
        # Extracts the athlete ID from the Athlete Link URL
        athlete_id = athlete_link.split('/')[-2]
        image_path = f"images/{athlete_id}.jpg"
        
        html_content += f"""
            <div class="athlete">
                <h3>{result[2]}</h3>
                <p>Place: {result[0]}</p>
                <p>Grade: {result[1]}</p>
                <p>Time: {result[4]}</p>
                <p>Team: {result[5]}</p>
                <img src="{image_path}" alt="Profile Picture of {result[2]}" width="150">
            </div>
            <hr>
        """

# Closing the individual results section and main content
html_content += """
        </section>
    </main>
    <footer id="main-footer">
        <p>&copy; 2024 Client Project - All rights reserved.</p>
    </footer>
</body>
</html>
"""

# Save the HTML content to a file
html_file_path = 'results.html'
try:
    with open(html_file_path, 'w') as file:
        file.write(html_content)
    print(f'HTML file generated: {html_file_path}')
except Exception as e:
    raise IOError(f"Error writing to the file: {e}")