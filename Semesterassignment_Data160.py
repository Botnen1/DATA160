
print('Oppgave A')
import pandas as pd

dartbase = pd.read_xml('dartbase.xml', xpath='.//spiller')
red_lion_players = dartbase[dartbase['stampub'] == 'Red Lion']
spillere = red_lion_players['navn'].tolist()

print(spillere)


print('Oppgave B')

import xml.etree.ElementTree as ET
import pandas as pd

# Function to extract pub records from the XML file
def parse_pubs(xml_root):
    pub_records = []

    for pub in xml_root.findall('pub'):
        pub_name = pub.find('navn').text if pub.find('navn') is not None else None
        pub_record = pub.find('pubrekord')
        record = pub_record.text if pub_record is not None else None
        record_holder = pub_record.get('rekordholder') if pub_record is not None else None

        if pub_name and record and record_holder:
            pub_records.append({'Pub': pub_name, 'Record': record, 'Record Holder': record_holder})

    return pd.DataFrame(pub_records)

# Load and parse the 'dartBase.xml' file
dart_base_path = 'dartBase.xml'  # Update this path to the location of XML file
tree = ET.parse(dart_base_path)
root = tree.getroot()

# Extract pub records and create a DataFrame
pub_records_df = parse_pubs(root)

print(pub_records_df.head())



print('Oppgave C')

import pandas as pd

def find_record_holder_and_regular_pub(xml_root, pub_name):
    # Find the record holder at the specified pub
    record_holder = None
    for pub in xml_root.findall('pub'):
        if pub.find('navn').text == pub_name:
            pub_record = pub.find('pubrekord')
            if pub_record is not None:
                record_holder = pub_record.get('rekordholder')
            break

    # Find the regular pub of the record holder
    regular_pub = None
    if record_holder:
        for player in xml_root.findall('spiller'):
            if player.find('navn').text == record_holder:
                regular_pub = player.get('stampub')
                break

    return record_holder, regular_pub

# Find the record holder and their regular pub at 'Red Lion'
record_holder, regular_pub = find_record_holder_and_regular_pub(root, 'Red Lion')

# Display the result in the requested format
f"{record_holder} : {regular_pub}"



print('Oppgave D')

import pandas as pd
def find_regular_patrons(xml_root):
    pub_patrons = {}

    # Collect the regular patrons for each pub
    for player in xml_root.findall('spiller'):
        pub_name = player.get('stampub')
        player_name = player.find('navn').text if player.find('navn') is not None else None

        if pub_name and player_name:
            if pub_name not in pub_patrons:
                pub_patrons[pub_name] = [player_name]
            else:
                pub_patrons[pub_name].append(player_name)

    return pub_patrons

# Find the regular patrons for each pub
regulars = find_regular_patrons(root)

# Display the result
regulars


print('Oppgave E')

# Function to find the names of event organizers at specified pubs

def find_event_organizers(xml_root, pubs):
    organizers = {pub: set() for pub in pubs}

    for pub in xml_root.findall('pub'):
        pub_name = pub.find('navn').text if pub.find('navn') is not None else None
        if pub_name in pubs:
            for tournament in pub.findall('turnering'):
                organizer = tournament.get('ansvarlig')
                if organizer:
                    organizers[pub_name].add(organizer)

    return organizers

# Pubs of interest
pubs_of_interest = ['Red Lion', 'Ye Olde Inn']

# Find the event organizers for 'Red Lion' and 'Ye Olde Inn'
event_organizers = find_event_organizers(root, pubs_of_interest)

# Display the result
event_organizers



print('Oppgave F')

# Function to find the player(s) with the highest score in a single tournament

def find_top_scorer(xml_root):
    highest_score = 0
    top_scorers = []

    # Find the highest score in any tournament
    for tournament in xml_root.findall('.//turnering/deltakelse'):
        score = int(tournament.get('poengsum'))
        if score > highest_score:
            highest_score = score
            top_scorers = [tournament.get('spiller')]
        elif score == highest_score:
            top_scorers.append(tournament.get('spiller'))

    # Find details of the top scorers
    top_scorer_details = []
    for player in xml_root.findall('spiller'):
        if player.find('navn').text in top_scorers:
            player_name = player.find('navn').text
            player_gender = player.find('kjønn').text
            player_age = player.find('alder').text
            top_scorer_details.append({'Name': player_name, 'Gender': player_gender, 'Age': player_age})

    return top_scorer_details

# Find the top scorer(s) in a single tournament
top_scorer_details = find_top_scorer(root)

# Display the result
top_scorer_details



print('Oppgave G')

# Function to find players who scored more than 1000 points in week 4

def find_high_scorers_in_week(xml_root, week):
    high_scorers = []

    # Find players who scored more than 1000 points in the specified week
    for tournament in xml_root.findall('.//turnering'):
        if tournament.get('UkeNr') == str(week):
            for participation in tournament.findall('deltakelse'):
                score = int(participation.get('poengsum'))
                if score > 1000:
                    player_name = participation.get('spiller')
                    high_scorers.append(player_name)

    return high_scorers

# Week of interest
week_of_interest = 4

# Find high scorers in week 4
high_scorers_week_4 = find_high_scorers_in_week(root, week_of_interest)

# Display the result
high_scorers_week_4



print('Oppgave H')
# Function to find the player(s) with the highest total points over the year

from collections import defaultdict

def find_top_scorers_over_year(xml_root):
    total_scores = defaultdict(int)

    # Sum the total points for each player
    for participation in xml_root.findall('.//turnering/deltakelse'):
        player_name = participation.get('spiller')
        score = int(participation.get('poengsum'))
        total_scores[player_name] += score

    # Find the highest total score
    highest_score = max(total_scores.values())

    # Find player(s) with the highest total score
    top_scorers = [player for player, score in total_scores.items() if score == highest_score]

    return top_scorers

# Find the top scorer(s) over the year
top_scorers_over_year = find_top_scorers_over_year(root)

# Display the result
top_scorers_over_year



print('Oppgave I')

# Function to find female players under 20 who scored at least 600 points at least twice

def find_young_female_high_scorers(xml_root):
    # Identifying female players under 20
    young_females = {}
    for player in xml_root.findall('spiller'):
        if player.find('kjønn').text == 'K' and int(player.find('alder').text) < 20:
            young_females[player.find('navn').text] = 0

    # Counting the number of times they scored 600 or more points
    for participation in xml_root.findall('.//turnering/deltakelse'):
        player_name = participation.get('spiller')
        score = int(participation.get('poengsum'))
        if player_name in young_females and score >= 600:
            young_females[player_name] += 1

    # Filtering for those who achieved this at least twice
    high_scorers = [player for player, count in young_females.items() if count >= 2]

    return high_scorers

# Find young female players who scored at least 600 points at least twice
young_female_high_scorers = find_young_female_high_scorers(root)

# Display the result
young_female_high_scorers



print('Oppgave J')

# Function to find players who did not participate in week 3

def find_non_participants_week_3(xml_root):
    # Identifying players who participated in week 3
    participants_week_3 = set()
    for tournament in xml_root.findall('.//turnering'):
        if tournament.get('UkeNr') == '3':
            for participation in tournament.findall('deltakelse'):
                participants_week_3.add(participation.get('spiller'))

    # Identifying all players and checking for non-participants in week 3
    non_participants = []
    for player in xml_root.findall('spiller'):
        player_name = player.find('navn').text
        player_age = player.find('alder').text
        if player_name not in participants_week_3:
            non_participants.append({'Name': player_name, 'Age': player_age})

    return non_participants

# Find players who did not participate in week 3
non_participants_week_3 = find_non_participants_week_3(root)

# Display the result
non_participants_week_3



print('Oppgave 2')

import xml.etree.ElementTree as ET

# Function for 'Oppgave 2'
import xml.etree.ElementTree as ET

def kontaktinfo(dartbase_root, kontakter_root, week):
    # Find the pub and organizer for the specified week
    pub_name, organizer_name = None, None
    for pub in dartbase_root.findall('.//pub'):
        for tournament in pub.findall('turnering'):
            if tournament.get('UkeNr') == str(week):
                pub_name = pub.find('navn').text
                organizer_name = tournament.get('ansvarlig')
                break
        if pub_name is not None:
            break

    # Find contact details for the pub and the organizer
    pub_address, pub_phone, organizer_phone = None, None, None
    if pub_name:
        for pub in kontakter_root.findall('.//pub'):
            if pub.find('navn').text == pub_name:
                pub_address = pub.find('adresse').text
                pub_phone = pub.find('telefon').text
                break

    if organizer_name:
        for person in kontakter_root.findall('.//person'):
            if person.find('navn').text == organizer_name:
                organizer_phone = person.find('telefon').text
                break

    result = f"Turneringen i uke {week}\n- pub: {pub_name}, {pub_address}, {pub_phone}\n- ansvarlig: {organizer_name}, {organizer_phone}"
    return result

# Load and parse the 'dartBase.xml' file
dartbase_path = 'dartBase.xml'  # Replace with the correct path
dartbase_tree = ET.parse(dartbase_path)
dartbase_root = dartbase_tree.getroot()

# Load and parse the 'kontakter.xml' file
kontakter_path = 'kontakter.xml'  # Replace with the correct path
kontakter_tree = ET.parse(kontakter_path)
kontakter_root = kontakter_tree.getroot()

# Call the function and print the result
week_of_interest = 6  # Replace with the desired week
result = kontaktinfo(dartbase_root, kontakter_root, week_of_interest)
print(result)



print('oppgave 3')

import pandas as pd

regnskap_df = pd.read_excel('regnskap.xlsx')  

highest_income_pub = regnskap_df.groupby('pub')['inntekt'].sum().idxmax()
highest_income_value = regnskap_df.groupby('pub')['inntekt'].sum().max()
print(f"Task A: The pub with the highest total income is {highest_income_pub} with {highest_income_value} pounds.")


all_weeks = set(range(1, regnskap_df['uke'].max() + 1))
recorded_weeks = set(regnskap_df['uke'])
missing_weeks = all_weeks - recorded_weeks
print(f"Task B: The following weeks are missing in the records: {sorted(missing_weeks)}")



# Read the XML file containing the tournament participation data
import xml.etree.ElementTree as ET

dartbase_xml_path = 'dartBase.xml'

# Load and parse the XML file
tree = ET.parse(dartbase_xml_path)
root = tree.getroot()

def extract_participation_data(xml_root):
    participation_data = {}
    
    # Iterate over each pub in the XML
    for pub in xml_root.findall('pub'):
        pub_name = pub.find('navn').text
        # Iterate over each tournament
        for tournament in pub.findall('turnering'):
            week = int(tournament.get('UkeNr'))
            # Count the number of participants in the tournament
            num_participants = len(tournament.findall('deltakelse'))
            # Store the data
            participation_data[(week, pub_name)] = num_participants
    
    return participation_data

# Extract the participation data
participation_data = extract_participation_data(root)

# Read the Excel file containing the income data
regnskap_df = pd.read_excel('regnskap.xlsx')

participation_fee = 10

discrepancy_df = regnskap_df.copy()
discrepancy_df['ExpectedIncome'] = discrepancy_df.apply(lambda row: participation_data.get((row['uke'], row['pub']), 0) * participation_fee, axis=1)
discrepancy_df['Discrepancy'] = discrepancy_df['ExpectedIncome'] - discrepancy_df['inntekt']

discrepancy_df.drop('ExpectedIncome', axis=1, inplace=True)

# Save the result  a new Excel file
discrepancy_output_path = 'avvik.xlsx'
discrepancy_df.to_excel(discrepancy_output_path, index=False)

discrepancy_output_path
