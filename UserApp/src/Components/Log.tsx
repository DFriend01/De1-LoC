/* Relative Imports */
import { Log } from '../State/UserState/UserState';

/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React from 'react';
import { View } from 'react-native';
import { Text } from 'react-native-paper';


const LogView : React.FC<{
    log: Log
}> = ({ log }) => (
    <View style={{
        borderColor: 'blue',
        backgroundColor: "lightskyblue",
        borderWidth: 4,
        margin: 5,
        padding: 5,
        borderRadius: 20,
    }}>
        <Text
            style={{
                textAlign: 'center',
                fontWeight: 'bold'
            }}
        >
            {`${log.username} used ${log.codename}`}
        </Text>
        <Text>
            {
                (log.success ? "Successfully unlocked" : "Attempted to unlock") + " the door at "
                + log.verifTime + " on " + log.verifDate +"."
            } 
        </Text>
    </View>
)

export default LogView;