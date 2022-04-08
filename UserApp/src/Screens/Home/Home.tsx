/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React, { Dispatch, SetStateAction } from 'react';
import { createMaterialBottomTabNavigator } from '@react-navigation/material-bottom-tabs';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
/* Relative Imports */
import Dashboard from './Dashboard';
import Settings from '../Settings/Settings';
import FaceID from '../FaceID/FaceID';
import CodeManagement from '../CodeManagement/CodeManagement';
import { UserState } from '../../State/UserState/UserState';

const Tab = createMaterialBottomTabNavigator();

const Home: React.FC<{
    user: UserState,
    updateUser: Dispatch<SetStateAction<UserState>>
    navigation: any
}> = ({ user, updateUser, navigation }) => {
    return <Tab.Navigator
        initialRouteName="Dashboard"
    >
        <Tab.Screen
            name="Dashboard"
            options={{
                tabBarLabel: "Home",
                tabBarIcon: ({ color }) => (
                    <MaterialCommunityIcons name="home" color={color} size={26} />
                )
            }}
        >
            {() => (
                <Dashboard
                    updateUser={updateUser}
                    user={user}
                />
            )}
        </Tab.Screen>
        <Tab.Screen
            name="FaceID"
            options={{
                tabBarLabel: "FaceID",
                tabBarIcon: ({ color }) => (
                    <MaterialCommunityIcons name="camera" color={color} size={26} />
                )
            }}
        >
            {() => (
                <FaceID
                    user={user}
                    updateUser={updateUser}
                    navigation={navigation}
                />
            )}
        </Tab.Screen>
        <Tab.Screen
            name="Code"
            options={{
                tabBarLabel: "Manage Codes",
                tabBarIcon: ({ color }) => (
                    <MaterialCommunityIcons name="home-lock-open" color={color} size={26} />
                )
            }}
        >
            {() => (
                <CodeManagement
                    user={user}
                    updateUser={updateUser}
                />
            )}
        </Tab.Screen>
        <Tab.Screen
            name="Settings"
            options={{
                tabBarLabel: "Settings",
                tabBarIcon: ({ color }) => (
                    <MaterialCommunityIcons name="cog" color={color} size={26} />
                )
            }}
        >
            {({ navigation }) => (
                <Settings
                    navigation={navigation}
                    user={user}
                />
            )}
        </Tab.Screen>
    </Tab.Navigator>
}

export default Home;