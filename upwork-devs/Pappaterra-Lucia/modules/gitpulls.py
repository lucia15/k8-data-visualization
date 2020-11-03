import json
import requests
import sys
import pandas as pd


class gitPulls ():

    def __init__(self, config):

        with open(config) as f:
            data = json.load(f)
        
        self.username = data["gituser"]
        self.token = data ["token"]
        self.url = data["url"]
        self.session = requests.Session()
        self.repositories = self.get_repos()

        
    def get_repos(self):
        url = 'https://api.github.com/users/k8-proxy/repos'      
        try:
            repos = pd.DataFrame(self.session.get(url=url).json())
            return repos['name'].apply(lambda s: 'k8-proxy/'+s if isinstance(s, str) else s).to_list()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)          


    def getPullRequests(self):
    
        d = []

        for repo in self.repositories:
            #print ("\n:::::Fetching pull requests from " + repo)

            try:
                temp_url = self.url + repo + "/pulls"
                req = requests.get(temp_url, auth=(self.username, self.token))
                data = req.json()

                try:
                    print("Error! A message from github server: \n" + data["message"])
                    break
                except:
                    #print("Success!")
                    empty = True
                    counter = 0

                    for pullRequest in data:
                    
                        link = pullRequest["html_url"]
                        name = pullRequest["base"]["repo"]["name"]
                        date = str(pullRequest["created_at"])

                        empty = False
                        counter = counter + 1
                        #print("\n:" + str(counter))
                        #print("PR Link: " + link)

                        #print("Repository Name: " + name)

                        all_reviewers = ""
                        for reviewer in pullRequest["requested_reviewers"]:
                            all_reviewers += reviewer["login"] + ", "

                        if (all_reviewers == ""):
                            all_reviewers = "not assigned"
                        else:
                            all_reviewers = all_reviewers[:-2]                            
                            
                        all_labels = ""
                        for label in pullRequest["labels"]:
                            all_labels += label["name"] + ", "

                        if (all_labels == ""):
                            all_labels = "none"
                        else:
                            all_labels = all_labels[:-2]    
                                     
                        #print("Reviewer(s): " + all_reviewers)
                        #print("Label(s): " + all_labels)
                        #print("Date Created: " + date)
                        
                        d.append([name, link, all_reviewers, all_labels, date])

                    #if (empty):
                        #print("\n:0")
                        #print("\nThere are no pull requests in " + repo)

            except:
                print("\nUnexpected error: ", sys.exc_info()[0])

        df = pd.DataFrame(d, columns=['Repository Name', 'PR Link', 'Reviewer(s)', 'Label(s)','Date Created'])
    
        return df
                