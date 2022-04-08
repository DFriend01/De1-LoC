/* Relative Imports */
import { UserState } from '../../State/UserState/UserState';
import { SetStateCallback } from '../../Components/useStateCallback';
import FaceScan from './ScanScreen';
import UnlockSuccess from '../Home/UnlockSuccess';
/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const FaceID: React.FC<{
    user: UserState,
    updateUser: SetStateCallback,
    navigation: any
}> = ({ user, updateUser, navigation }) => {
    const Stack = createNativeStackNavigator();
    return (
        <Stack.Navigator
            initialRouteName='FaceScan'
            screenOptions={{ headerShown: false }}
        >
            <Stack.Screen
                name="FaceScan"
            >
                {({ navigation }) => (
                    <FaceScan
                        navigation={navigation}
                        user={user}
                        updateUser={updateUser}
                    />
                )}
            </Stack.Screen>
            <Stack.Screen
                name="Success"
            >
                {({ navigation }) => (
                    <UnlockSuccess
                        navigation={navigation}
                        screen="FaceScan"
                    />
                )}

            </Stack.Screen>
        </Stack.Navigator>
    )
}

export default FaceID;