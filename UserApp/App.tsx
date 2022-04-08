/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * Generated with the TypeScript template
 * https://github.com/react-native-community/react-native-template-typescript
 *
 * @format
 */

import React, { useEffect, useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  useColorScheme,
  View,
} from 'react-native';

import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import {
  Colors,
  DebugInstructions,
  Header,
  LearnMoreLinks,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';

import AccountManagement from './src/Screens/UserAccountManagement/AM';
import Home from './src/Screens/Home/Home';
import { initialUser } from './src/State/UserState/UserState';
import getCameraPermission from './src/Async/permissions';
import useStateCallback from './src/Components/useStateCallback';
import messaging from '@react-native-firebase/messaging';
import notifee from '@notifee/react-native';

const onMessageReceived = async (message : any) => {
  const channelId = await notifee.createChannel({
    id: "default",
    name: "default channel"
});
  if (!message.data.username) {
    console.log("notification received");
    console.log(message)
  
  return notifee.displayNotification({
    title: "Test Notification!",
    body: "This is a test of Firebase",
    android: {
      channelId
    }
  })
  } else {
    await notifee.displayNotification({
      title: "Anomaly Detected!",
      body: `${message.data.username} unlocked the door using ${message.data.codename}`,
      android: {
        channelId
      }
    })
  }

  
  // const promise = new Promise((resolve, reject) => {
    
    // if (!message.data.username) {
    //   console.log("notification received");
    //   notifee.displayNotification({
    //     title: "Test Notification",
    //     body: "This is a test of Firebase"
    //   })
    // } else {
    //   notifee.displayNotification({
    //     title: "Anomaly Detected!",
    //     body: `${message.data.username} unlocked the door using ${message.data.codename}`
    //   });
    // }
    // if(true) {
    //   resolve("Yay!");
    // } else {
    //   reject("Nay");
    // }

  // });
  // return promise;
}
messaging().onMessage(onMessageReceived);
//messaging().setBackgroundMessageHandler(onMessageReceived);

const App = () => {
  const [user, setUser] = useStateCallback(initialUser);
  const [userToken, setUserToken] = useState("");
  const Stack = createNativeStackNavigator();
  console.log("rendering");
  const onStart = async () => {
    await messaging().registerDeviceForRemoteMessages();
    const token = await messaging().getToken();
    setUserToken(token);
    console.log(token);
  }
  getCameraPermission();

  useEffect(() => {
    onStart();
  }, [])


  return (
      <NavigationContainer>
        <Stack.Navigator initialRouteName="AM" screenOptions={{headerShown: false}}>
          <Stack.Screen name="AM">
            {() => (
              <AccountManagement
                token={userToken}
                user={user}
                updateUser={setUser}
              />
            )}
          </Stack.Screen>
          <Stack.Screen name="Home">
              {
                ({navigation}) => (
                  <Home
                    user={user}
                    updateUser={setUser}
                    navigation={navigation}
                  />
                )
              }
          </Stack.Screen>
        </Stack.Navigator>
      </NavigationContainer>
  );
};

// const styles = StyleSheet.create({
//   sectionContainer: {
//     marginTop: 32,
//     paddingHorizontal: 24,
//   },
//   sectionTitle: {
//     fontSize: 24,
//     fontWeight: '600',
//   },
//   sectionDescription: {
//     marginTop: 8,
//     fontSize: 18,
//     fontWeight: '400',
//   },
//   highlight: {
//     fontWeight: '700',
//   },
// });

export default App;
