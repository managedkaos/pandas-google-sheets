import pandas
import ConfigParser
from ftplib import FTP

# read the config file and assign values
config = ConfigParser.ConfigParser()
config.read('config.txt')

gsheet_url = config.get('gsheet','url')
ftp_host   = config.get('ftp','host')
ftp_user   = config.get('ftp','user')
ftp_pass   = config.get('ftp','pass')

# remove the column bounds
pandas.set_option('display.expand_frame_repr', False)

# get the data or die
p = pandas.read_csv(gsheet_url)

# open ftp or die
ftp = FTP(ftp_host)
ftp.login(ftp_user, ftp_pass)

# incoming column number and names
# 0  'Timestamp',
# 1  'First Name',
# 2  'Last Name',
# 3  'Phone Number (in xxx-xxx-xxxx format)',
# 4  'Phone Number Type',
# 5  'Preferred Email Address',
# 6  'Street Address',
# 7  'City',
# 8  'ZIP Code',
# 9  'Contact Preference',
# 10 'Birth Month/Day (in MM/DD format)',
# 11 'Initiation Date',
# 12 'Wedding Anniversary Month/Day (in MM/DD format)',
# 13 'Target Committees (select at least one)',
# 14 'Additional Committees (select no more than three)'

target_committees = [ 
    'Educational Enrichment',
    'Environmental Ownership',
    'Family Strengthening',
    'Global Impact',
    'Health Promotion'
]

additional_committees = [
    'AKA Connection',
    'Archives',
    'Audit',
    'Awards',
    'Black Heritage',
    'Budget-Finance',
    'Chapter Relations',
    'Communications',
    'Constitution & By-Laws',
    'Diamond & Golden Soror Concerns',
    'Education/Scholarship',
    'Educational Advancement Foundation',
    'Fine Arts',
    "Founders' Day",
    'History',
    'Hospitality',
    'Membership',
    'Nominating',
    'Pan Hellenic Counsel',
    'Program',
    'Protocol',
    'Public Relations',
    'Reading is Fundamental',
    'Sisterly Relations',
    'Social',
    'Special Projects',
    'Standards & Evaluations',
    'Strategic Planning',
    'Technology',
    'Tellers',
    'Time & Place',
    'Ways and Means',
    'Yearbook'
]


# simplify the column names
p.rename(columns={'Phone Number (in xxx-xxx-xxxx format)':'Phone Number'}, inplace=True)
p.rename(columns={'Birth Month/Day (in MM/DD format)':'Birth Month/Day'}, inplace=True)
p.rename(columns={'Wedding Anniversary Month/Day (in MM/DD format)':'Wedding Anniversary'}, inplace=True)
p.rename(columns={'Target Committees (select at least one)':'Target Committees'}, inplace=True)
p.rename(columns={'Additional Committees (select no more than three)':'Additional Committees'}, inplace=True)

# drop duplicates by email address
p.drop_duplicates('Preferred Email Address', inplace=True)

# print all member details, sorted by last name
print "All members..."
p.iloc[:, 1:9].sort_values(by=['Last Name'], ascending=True).to_csv('members.csv')
p.iloc[:, 1:9].sort_values(by=['Last Name'], ascending=True).to_html('members.html')
ftp.storlines('STOR ' + 'members.html', open ('members.html'))
ftp.storlines('STOR ' + 'members.csv', open ('members.csv'))

# print target committees with member details
print "Target committees..."
for committee in target_committees:
    committee_filename = ''.join(e for e in committee if e.isalnum())    
    pslice = p[ p['Target Committees'].str.contains(committee, na=False) ]
    pslice.iloc[:, 1:9].sort_values(by=['Last Name'], ascending=True).to_csv(committee_filename + '.csv')
    pslice.iloc[:, 1:9].sort_values(by=['Last Name'], ascending=True).to_html(committee_filename + '.html')
    ftp.storlines('STOR ' + committee_filename + '.html', open (committee_filename + '.html'))
    ftp.storlines('STOR ' + committee_filename + '.csv', open (committee_filename + '.csv'))

# print additional committees with member details
print "Additional committees..."
for committee in additional_committees:
    committee_filename = ''.join(e for e in committee if e.isalnum())
    pslice = p[ p['Additional Committees'].str.contains(committee, na=False) ]
    pslice.iloc[:, 1:9].sort_values(by=['Last Name'], ascending=True).to_csv(committee_filename + '.csv')
    pslice.iloc[:, 1:9].sort_values(by=['Last Name'], ascending=True).to_html(committee_filename + '.html')
    ftp.storlines('STOR ' + committee_filename + '.html', open (committee_filename + '.html'))
    ftp.storlines('STOR ' + committee_filename + '.csv', open (committee_filename + '.csv'))
