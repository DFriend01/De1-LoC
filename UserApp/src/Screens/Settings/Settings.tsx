/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React from 'react';
import { Button, Text, Title } from 'react-native-paper';
import { SafeAreaView } from 'react-native';
/* Relative Imports */
import { UserState } from '../../State/UserState/UserState';
import { logout } from '../../Networking/AuthManagement';

const Settings: React.FC<{
    navigation: any,
    user: UserState
}> = ({ navigation, user }) => {
    const onSubmit = () => {
        const onSuccess = () => {
            navigation.navigate("Login");
        }
        const onFailure = (e: string) => {
            console.log(e);
        }
        logout(onSuccess, onFailure)
    }
    return (
        <SafeAreaView
            style={{
                alignItems: "center",
                paddingTop: 10
            }}
        >
            <Title>
                {`${user.profile.firstname} ${user.profile.lastname}`}
            </Title>
            <Title>
                {user.profile.username}
            </Title>
            <Button
                style={{
                    marginTop: 20
                }}
                color="blue"
                mode="contained"
                onPress={onSubmit}
            >
                Logout
            </Button>
        </SafeAreaView>
    );
}

export default Settings;