/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React, { Dispatch, SetStateAction } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
/* Relative Imports */
import Login from './Login';
import UserRegistration from './Register';
import { UserState } from '../../State/UserState/UserState';

const AccountManagement: React.FC<{
    user: UserState,
    updateUser: Dispatch<SetStateAction<UserState>>,
    token: string
}> = ({token, user, updateUser}) => {
    const Stack = createNativeStackNavigator();
    return (
        <Stack.Navigator
            initialRouteName="Login"
            screenOptions={{ headerShown: false }}
        >
            <Stack.Screen name="Login">
                {
                    ({navigation}) => (
                        <Login
                            updateUser={updateUser}
                            user={user}
                            navigation={navigation}
                            token={token}
                        />
                    )
                }
            </Stack.Screen>
            <Stack.Screen name="Register" component={UserRegistration} />
        </Stack.Navigator>
    )
};

export default AccountManagement;