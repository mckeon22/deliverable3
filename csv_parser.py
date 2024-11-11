import os

# Paths to files and folders
file_path = 'SEC_Jamboree_1_Womens_5000_Meters_Junior_Varsity_24.csv'
image_folder_path = 'images'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

# Function to generate HTML content for a given set of results
def generate_html(file_name, title, team_scores, individual_results):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <link rel="stylesheet" type="text/css" href="css/reset.css"> 
        <link rel="stylesheet" href="css/style.css">
        <title>{title}</title>
    </head>
    <body>
        <a href="#content" class="skip-link">Skip to main content</a>
        
        <header>
            <h1>Athlete Performance Tracker - {title}</h1>
        </header>
        <nav>
            <span class="hamburger" aria-label="Toggle navigation menu">&#9776;</span>
            <ul>
                <li><a href="female.html">Women</a></li>
                <li class="dropdown">
                    <a href="#" aria-haspopup="true">Grade Level</a>
                    <ul class="dropdown-content">
                        <li><a href="grade_9.html">Grade 9</a></li>
                        <li><a href="grade_10.html">Grade 10</a></li>
                        <li><a href="grade_11.html">Grade 11</a></li>
                    </ul>
                </li>
                <li><a href="results.html">Event Results</a></li>
            </ul>
        </nav>
        
        <!-- Filter Options -->
        <div id="filters">
            <label for="sortFilter">Sort By:</label>
            <select id="sortFilter" aria-label="Sort Athletes">
                <option value="default">Default</option>
                <option value="time">Time</option>
                <option value="alphabetical">Alphabetical Order</option>
                <option value="team">Team</option>
            </select>
        </div>

        <main id="content">
            <section id="event-title" tabindex="0">
                <h2>{title}</h2>
            </section>
            <section id="team-scores">
                <h3>Team Scores</h3>
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
    
    # Add only top 3 team scores to the HTML content
    for score in team_scores[:3]:
        if len(score) >= 3:
            html_content += f"""
                        <tr>
                            <td>{score[0]}</td>
                            <td>{score[1]}</td>
                            <td>{score[2]}</td>
                        </tr>
            """
    
    html_content += """
                    </tbody>
                </table>
            </section>
            <section id="individual-results">
                <h2>Results</h2>
                <div id="results-container">
    """
    
    # Loop through all individual results for female.html; only top 3 for results.html
    for idx, result in enumerate(individual_results):
        athlete_link = result[3]
        try:
            athlete_id = athlete_link.split('/')[-2]
            image_path = os.path.join(image_folder_path, f"{athlete_id}.jpg")
            if not os.path.exists(image_path):
                image_path = os.path.join(image_folder_path, "default.jpg")
        except IndexError:
            image_path = os.path.join(image_folder_path, "default.jpg")
        
        place_class = ["first-place", "second-place", "third-place"][idx] if idx < 3 else ""
        medal_color_class = ["gold-medal", "silver-medal", "bronze-medal"][idx] if idx < 3 else "no-medal"

        html_content += f"""
            <div class="athlete {place_class}" data-time="{result[4]}" data-name="{result[2]}" data-team="{result[5]}">
                <h3><i class="fas fa-medal {medal_color_class}"></i> {result[2]}</h3>
                <p><i class="fas fa-trophy icon"></i> Place: {result[0]}</p>
                <p><i class="fas fa-graduation-cap icon"></i> Grade: {result[1]}</p>
                <p><i class="fas fa-stopwatch icon"></i> Time: {result[4]}</p>
                <p><i class="fas fa-users icon"></i> Team: {result[5]}</p>
                <img src="{image_path}" alt="Profile Picture of {result[2]}" width="150">
            </div>
        """

    html_content += """
                </div>
            </section>

            <!-- Back to Top Button -->
            <button id="backToTop" class="back-to-top">Top</button>
        
        </main>
        <footer id="main-footer">
            <p>&copy; 2024 Client Project - All rights reserved.</p>
        </footer>

        <!-- Link to External JavaScript File -->
        <script src="js/script.js"></script>
    </body>
    </html>
    """
    
    with open(file_name, 'w') as file:
        file.write(html_content)
    print(f'{file_name} generated successfully.')

# Read CSV and parse data
try:
    with open(file_path, 'r') as file:
        lines = file.readlines()
except Exception as e:
    raise IOError(f"Error reading the file: {e}")

# Parse data into sections
team_scores = []
individual_results = []
in_team_scores = False
in_individual_results = False

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
    elif not line:
        continue

    data = line.split(',')
    if in_team_scores and len(data) >= 3:
        team_scores.append(data[:3])
    elif in_individual_results and len(data) >= 8:
        individual_results.append(data[:8])

# Generate the main results page with only the top 3 individual results
generate_html("results.html", "Event Results", team_scores[:3], individual_results[:3])

# Generate the female.html file with all individual results
generate_html("female.html", "Female Athletes", team_scores[:3], individual_results)

# Generate the grade-level pages with all individual results filtered by grade
grades = ["9", "10", "11"]
for grade in grades:
    filtered_results = [result for result in individual_results if result[1] == grade]
    generate_html(f"grade_{grade}.html", f"Grade {grade} Athletes", team_scores[:3], filtered_results)
