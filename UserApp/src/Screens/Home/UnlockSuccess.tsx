/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React from 'react';
import { SafeAreaView } from 'react-native';
import { Button, Title } from 'react-native-paper';

const UnlockSuccess: React.FC<{
    navigation: any
    screen: string
}> = ({
    navigation,
    screen
}) => {
        return (
            <SafeAreaView
                style={{
                    margin: 10,
                    flexDirection: "column",
                    justifyContent: "center"
                }}
            >
                <Title
                    style={{
                        textAlign: "center",
                        marginBottom: 10
                    }}
                >
                    Unlock Successful. Press the button on the De1-LoC now to initiate the unlock
                </Title>
                <Button
                    mode="contained"
                    color="blue"
                    onPress={() => { navigation.navigate(screen) }}
                >
                    Go Home
                </Button>
            </SafeAreaView>
        )
    }

export default UnlockSuccess;