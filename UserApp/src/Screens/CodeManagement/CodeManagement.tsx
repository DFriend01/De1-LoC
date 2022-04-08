/* Relative Imports */
import DoorCodeRegister from './Register';
import { UserState } from '../../State/UserState/UserState';
import CodeList from './CodeList';
/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React, { Dispatch, SetStateAction } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';


const CodeManagement: React.FC<{
    user: UserState,
    updateUser: Dispatch<SetStateAction<UserState>>
}> = ({ user, updateUser }) => {
    const Stack = createNativeStackNavigator();
    return (
        <Stack.Navigator
            initialRouteName='CodeList'
            screenOptions={{ headerShown: false }}
        >
            <Stack.Screen
                name={"CodeList"}
            >
                {({ navigation }) => (
                    <CodeList
                        navigation={navigation}
                        user={user}
                        updateUser={updateUser}
                    />
                )}
            </Stack.Screen>
            <Stack.Screen
                name={"AddCode"}
            >
                {({ navigation }) => (
                    <DoorCodeRegister
                        navigation={navigation}
                        user={user}
                        updateUser={updateUser}
                    />
                )}

            </Stack.Screen>
        </Stack.Navigator>
    );
}
export default CodeManagement;