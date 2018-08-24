import os
import csv

shpollpath = os.path.join('Resources', 'election_data.csv')

with open(shpollpath, newline='') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')

    header = next(csvreader)

    total_votes = [] 
    final_total_votes =[]
    names = []
    percent_vote = []
    candidates_names_and_votes = {}       
    final_names_and_votes = []
    winner = []
    final_list = []
    final = []
    
    for row in csvreader:
        
        total_votes.append(row[2])

        if row[2] not in candidates_names_and_votes.keys():

            candidates_names_and_votes[row[2]] = 1

        else:

            candidates_names_and_votes[row[2]] +=1
    
    for v in candidates_names_and_votes.values():

        percent_vote.append(round(int(v)*100/len(total_votes)))

    print(f"The total number of votes cast is: {str(len(total_votes))}")

    print(f"The complete list of candidates who received votes is: {list(candidates_names_and_votes)}")
    
    print(f"The percentage of votes each candidate won respectively is: {percent_vote}")

    print(f"The total number of votes each candidate won is: {candidates_names_and_votes}")

    print(f"The winnes is: {max(candidates_names_and_votes, key=candidates_names_and_votes.get)}")


    names.append(list(candidates_names_and_votes))
    final_total_votes = str(len(total_votes))
    final_names_and_votes = candidates_names_and_votes
    winner = (max(candidates_names_and_votes, key=candidates_names_and_votes.get))

final_list = [final_total_votes, names, percent_vote, final_names_and_votes, winner]
final = zip(final_list)

output_file = os.path.join("output.csv")

with open(output_file, "w", newline="") as datafile:

	writer = csv.writer(datafile)

	writer.writerow(["Total Votes", "Names", "Vote Percetage", "Vote of Each Candidate", "Winner"])

	writer.writerow(final)