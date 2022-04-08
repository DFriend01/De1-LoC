/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import React from 'react';
/* Relative Imports */
import { SetStateCallback } from '../../Components/useStateCallback';
import { UserState } from '../../State/UserState/UserState';
import DashboardScreen from './DashboardScreen';
import Unlock from './Unlock';
import UnlockSuccess from './UnlockSuccess';

const Dashboard: React.FC<{
    user: UserState,
    updateUser: SetStateCallback
}> = ({ user, updateUser }) => {
    const Stack = createNativeStackNavigator();
    return (
        <Stack.Navigator
            initialRouteName="DashboardScreen"
            screenOptions={{ headerShown: false }}
        >
            <Stack.Screen
                name="DashboardScreen"
            >
                {({ navigation }) => (
                    <DashboardScreen
                        navigation={navigation}
                        user={user}
                        updateUser={updateUser}

                    />
                )}
            </Stack.Screen>
            <Stack.Screen
                name="Unlock"
            >
                {({ navigation }) => (
                    <Unlock
                        navigation={navigation}
                        user={user}
                    />
                )}

            </Stack.Screen>
            <Stack.Screen
                name="Success"
            >
                {({ navigation }) => (
                    <UnlockSuccess
                        navigation={navigation}
                        screen="DashboardScreen"
                    />
                )}
            </Stack.Screen>
        </Stack.Navigator>
    )
}

export default Dashboard;