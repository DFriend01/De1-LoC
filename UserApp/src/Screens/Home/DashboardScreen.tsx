import React, { EffectCallback, useEffect } from 'react';
import { View, SafeAreaView, ScrollView } from 'react-native';
import { Button, Text, Title } from 'react-native-paper';
import { SetStateCallback } from '../../Components/useStateCallback';
import { getLogs, getNextLogs } from '../../Networking/LogManagement';
import { UserState, Log } from '../../State/UserState/UserState';
import  LogView from '../../Components/Log';
import notifee from '@notifee/react-native';

const DashboardScreen : React.FC<{
    navigation: any,
    user: UserState,
    updateUser: SetStateCallback
}> = ({navigation, user, updateUser}) => {
    const handleSubmit = () => {
        navigation.navigate("Unlock");
    }
    const handleRefresh = () => {
        const onSuccess = (logs: Object) => {
            updateUser({
                ...user,
                logs: Object.values(logs),
                logOffset: Object.keys(logs).length
            })
        }
        const onFailure = (e: string) => {
            console.log(e);
        }
        getLogs(onSuccess, onFailure);
    }
    const handleGetNext = () => {
        const onSuccess = (logs: Object) => {
            updateUser({
                ...user,
                logs: [...user.logs, ...Object.values(logs)],
                logOffset: user.logOffset + Object.keys(logs).length
            })
        }
        const onFailure = (e: string) => {
            console.log(e);
        }
        getNextLogs(user.logOffset, onSuccess, onFailure);
    }
    const notificationTest = async () => {
        const channelId = await notifee.createChannel({
            id: "default",
            name: "default channel"
        });

        await notifee.displayNotification({
            title: "Alert",
            body: "Devon detected!",
            android: {
                channelId,
            }
        });
    }
    return (
        <SafeAreaView>
            <ScrollView>
            {/* <Button
                onPress={() => notificationTest()}
            >
                Notify
            </Button> */}
            <Title
                style={{
                    marginTop: 10,
                    marginBottom: 20,
                    textAlign: "center"
                }}
            >
                Activity History
            </Title>
            <View
                style={{
                    flexDirection: "row",
                    alignSelf: "center",
                    marginBottom: 10

                }}
            >
            <Button
                onPress={handleRefresh}
                mode="contained"
                color="blue"
                style={{
                    marginRight: 10,
                    width: 150
                }}
            >
                Refresh Feed
            </Button>
            <Button
                onPress={handleGetNext}
                mode="contained"
                color="blue"
                style={{
                    marginLeft: 10,
                    width: 150
                }}
            >
                Get more
            </Button>

            </View>

            {
            !user.logs? (<></>) : (
                user.logs.map(
                    (log: Log, index: number) => (
                        <LogView
                            key={index}
                            log={log}
                        />
                    )
                )
            )}
            
            <Button
                onPress={handleSubmit}
                mode="contained"
                color="blue"
                style={{
                    marginHorizontal: 75,
                    marginTop: 20,
                    marginBottom: 40
                }}
            >
                Unlock
            </Button>
            </ScrollView>
            
        </SafeAreaView>
    )
};

export default DashboardScreen;