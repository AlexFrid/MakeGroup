"""Replicates the make group tool in Alteryx"""

# Import necessary modules
import networkx as nx
import pandas as pd
from itertools import repeat
from networkx.algorithms import community


def makegroups(df):
    """
    Replicates the functionality of the make group tool in Alteryx
    Exepects a pandas dataframe ("df") with two columns.
    """
    try:
        # Renames df columns
        df.columns = ['a', 'b']

        # Converting the df to a list for network edges
        edgesList = df.values.tolist()

        # Converting the df to a dictionary for network nodes
        nodeDict = df.to_dict('list')

        # Creating an empty graph
        G = nx.Graph()

        # Adding nodes from both lists in the dictionary
        # Effectively a merge of the two lists
        G.add_nodes_from(nodeDict['a'])
        G.add_nodes_from(nodeDict['b'])

        # Adding the edges from the edges list
        G.add_edges_from(edgesList)

        # Generates groups
        # TODO check that size of smallest clique, here 2 is dynamic
        comm = list(community.k_clique_communities(G, 2))

        # Splits the communities into two lists
        comm1 = list(comm[0])
        comm2 = list(comm[1])

        # Generates list of the group name
        # Replicates the group name to match community list length
        group1 = list(repeat(comm1[0], len(comm1)))
        group2 = list(repeat(comm2[0], len(comm2)))

        # combines each group name and community list into a dataframe
        dfGroup1 = pd.DataFrame(list(zip(group1, comm1)), columns=['Group', 'key'])
        dfGroup2 = pd.DataFrame(list(zip(group2, comm2)), columns=['Group', 'key'])

        # Combines both dataframes into the final dataframe
        df = dfGroup1.append(dfGroup2, ignore_index=True)
        print("Success: Groups created")
        return df
    except Exception as e:
        print("Error: Function - makegroups:", e)
