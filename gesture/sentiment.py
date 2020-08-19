import pandas as pd
import spacy
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# setup for entity recognition and sentiment analysis
analyser = SentimentIntensityAnalyzer()
nlp = spacy.load('en_core_web_sm')


#Text parsing function
def is_word_present(given_string, given_word):
    return (' ' + given_word + ' ') in (' ' + given_string + ' ')


#Determining gesture based on identified action id
def mapping_action_id_to_action(given_id):
    mapped_action = 'straight'

    if given_id == 1:
        mapped_action = 'straight'
    elif given_id == 2:
        mapped_action = 'right'
    elif given_id == 3:
        mapped_action = 'left'
    elif given_id == 4:
        mapped_action = 'yes'
    elif given_id == 5:
        mapped_action = 'no'
    elif given_id == 6:
        mapped_action = 'happy'
    elif given_id == 7:
        mapped_action = 'sad'
    elif given_id == 8:
        mapped_action = 'idl1'
    elif given_id == 9:
        mapped_action = 'idl2'
    elif given_id == 10:
        mapped_action = 'idl3'
    elif given_id == 11:
        mapped_action = 'idl4'
    elif given_id == 12:
        mapped_action = 'idl5'
    elif given_id == 13:
        mapped_action = 'yes'

    return mapped_action


#Determining action id based on the dialogue
def determine_action_id(given_dialogue, given_additional):
    determined_id = 1

    if given_additional == 0:

        #Sentiment analysis for happy and sad
        if determined_id == 1:
            score = analyser.polarity_scores(given_dialogue)
            positive_score = score['pos']
            negative_score = score['neg']
            if positive_score >= 0.3 or negative_score >= 0.3:
                if positive_score > negative_score:
                    determined_id = 6
                else:
                    determined_id = 7

        #Checking for agreement and disagreement
        if determined_id == 1:
            if is_word_present(given_dialogue, 'yes') or is_word_present(given_dialogue, 'Yeah') \
                    or is_word_present(given_dialogue, 'Yes') or is_word_present(given_dialogue, 'yeah'):
                determined_id = 4

        if determined_id == 1:
            if is_word_present(given_dialogue, 'no') or is_word_present(given_dialogue, 'not') \
                    or is_word_present(given_dialogue, 'No') or is_word_present(given_dialogue, 'Not'):
                determined_id = 5


        #Spatial gesture people (add objects similarly)
        entity = nlp(given_dialogue)
        for ent in entity.ents:
            if ent.text == "Fungi":  # Fungi is the name of the robot
                determined_id = 2

        if is_word_present(given_dialogue, 'Fungi'):
            determined_id = 2

        if determined_id == 1:
            if is_word_present(given_dialogue, 'Blue'): #Blue is the name of the robot
                determined_id = 3

        if determined_id == 1:
            determined_id = random.randint(8, 12)

    #Punchline gesture
    elif given_additional in range(1, 4):
        determined_id = 13

    #Positive and negative question
    elif given_additional == 5:
        score = analyser.polarity_scores(given_dialogue)
        positive_score = score['pos']
        negative_score = score['neg']
        if negative_score > positive_score:
            determined_id = 5
        else:
            determined_id = 4

    return determined_id


#Writing into a csv file from dataframe
def write_into_output_df(given_df, given_time, given_action, given_dialogue, given_gesture_number):
    data = {'gesture_number': [given_gesture_number], 'time': [given_time], 'gesture': [given_action], 
        'speed': 1.0, 'amplitude': 1.0, 'dialogue': [given_dialogue]}
    df = pd.DataFrame(data)
    # result_df = pd.concat([given_df, df])
    result_df = given_df.append(df)
    return result_df

def create_gesture_output(file_name):
#Input dialogue file
    input_df = pd.read_csv(file_name)

    #Set default
    robot_id_current = 1
    robot_id_previous = 1

    #Initialize output dataframes
    output_data_robot1 = {'time': [], 'gesture': []}
    output_df_robot1 = pd.DataFrame(output_data_robot1)
    output_data_robot2 = {'time': [], 'gesture': []}
    output_df_robot2 = pd.DataFrame(output_data_robot2)

    for index, row in input_df.iterrows():
        speaker = row['speaker']
        time = row['time']
        dialogue = row['dialogue']
        additional = row['additional']
        gesture_number = row['gesture_number']
        if speaker == 1:
            robot_id_current = 1
            if robot_id_previous != robot_id_current:
                action_id_robot2 = 1
                action_robot2 = mapping_action_id_to_action(action_id_robot2)
                output_df_robot2 = write_into_output_df(output_df_robot2, time + 4, action_robot2, dialogue, gesture_number)
            action_id_robot1 = determine_action_id(dialogue, additional)
            print(dialogue)
            print(action_id_robot1)
            action_robot1 = mapping_action_id_to_action(action_id_robot1)
            output_df_robot1 = write_into_output_df(output_df_robot1, time + 8, action_robot1, dialogue, gesture_number)
            robot_id_previous = robot_id_current
        elif speaker == 2:
            robot_id_current = 2
            if robot_id_previous != robot_id_current:
                action_id_robot1 = 1
                action_robot1 = mapping_action_id_to_action(action_id_robot1)
                output_df_robot1 = write_into_output_df(output_df_robot1, time + 8, action_robot1, dialogue, gesture_number)
            action_id_robot2 = determine_action_id(dialogue, additional)
            print(dialogue)
            print(action_id_robot2)
            action_robot2 = mapping_action_id_to_action(action_id_robot2)
            output_df_robot2 = write_into_output_df(output_df_robot2, time + 4, action_robot2, dialogue, gesture_number)
            robot_id_previous = robot_id_current


    #Print output dataframes for testing
    print(output_df_robot1)
    print(output_df_robot2)

    #Write output into csv files
    export_csv = output_df_robot1.to_csv(r'Gesture_output1.csv', index=None, header=True)
    export_csv = output_df_robot2.to_csv(r'Gesture_output2.csv', index=None, header=True)
