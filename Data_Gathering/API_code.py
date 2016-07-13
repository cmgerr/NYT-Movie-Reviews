import urllib
import json
import pandas as pd
import numpy as np
from time import sleep

# API key and root url for API requests
apikey= # personal API key for NYT movie reviews here
urlroot = 'http://api.nytimes.com/svc/movies/v2/reviews/all.json'

# columns for all the data headers in API response
cols = ['byline', 'critics_pick', 'date_updated', 'display_title', 'headline',
    'link_suggested_link_text', 'link_type', 'link_url', 'mpaa_rating',
    'multimedia_height', 'multimedia_src', 'multimedia_type', 'multimedia_width',
    'opening_date', 'publication_date', 'summary_short']
NYTrev = pd.DataFrame(columns = cols)

offset = 0 # start at zero, re-set to where loop left off if API rate limit is hit
covered = [] # list to check offsets that have been captured

# loop to retrieve more reviews until either API rate limit is hit (1000/day), or
# there are no more results. Contents of reviews are added to DataFrame
while True:
    url = '%s?offset=%d&api-key=%s'% (urlroot, offset, apikey)
    data = urllib.urlopen(url)
    parsed_data = json.loads(data.read())
    if len(parsed_data) == 1: # this indicates that API rate limit was hit
        print 'Stopped at offset: ', offset
        break
    else:
        for i in range(len(parsed_data['results'])):
            row = pd.Series(index=cols)
            for j in parsed_data['results'][i]:
                k = parsed_data['results'][i][j]
                if type(k) == dict: # some values are nested within dictionaries
                    for m in k:
                        row[j+'_'+m] = k[m]
                else: row[j] = k
            NYTrev = NYTrev.append(row, ignore_index=True)
        covered.append(offset)
        print "Done offset:", offset # to show progress as code runs
        offset+=20 # there are 20 results per request, so jump up by 20 with each new call
        sleep(5) # NYT API has a minimum of 5 seconds between API requests
        if parsed_data['has_more'] ==  False: break # break loop if no more results exist


# check list of covered offsets:
print covered

# write results to CSV
NYTrev.to_csv('../../NYT_movie_reviews.csv', encoding='utf-8', index=False)
