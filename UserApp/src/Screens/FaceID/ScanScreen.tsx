/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import { useIsFocused } from '@react-navigation/native';
import React, { useState, useRef, } from 'react';
import { ActivityIndicator, Button, Title } from 'react-native-paper';
import { SafeAreaView, Text, View } from 'react-native';
import { Camera, CameraDevice, useCameraDevices } from 'react-native-vision-camera';
import { Asset, launchImageLibrary } from 'react-native-image-picker';
/* Relative Imports */
import { UserState } from '../../State/UserState/UserState';
import { SetStateCallback } from '../../Components/useStateCallback';
import { authFaceID, registerFace } from '../../Networking/FaceManagement';
import { EMULATOR } from '../../utils/config';


const FaceScan: React.FC<{
    user: UserState,
    updateUser: SetStateCallback,
    navigation: any
}> = ({
    user,
    updateUser,
    navigation
}) => {
        const [apiError, setApiError] = useState("");
        const [isUnlocking, setIsUnlocking] = useState(false);
        const onSuccess = () => {
            setIsUnlocking(false);
            navigation.navigate(
                "Success"
            )
        }
        const cameraRef = useRef<Camera>(null);
        const devices = useCameraDevices();
        const isActive = useIsFocused();
        const dev = EMULATOR ? devices.back : devices.front;
        const camera = (
            <View style={{ alignItems: 'center' }}>
                <Title
                    style={{ marginTop: 10 }}
                >
                    Face ID
                </Title>
                <View>
                    {user.profile.face_enabled ? (
                        <>
                            <Camera
                                ref={cameraRef}
                                isActive={isActive}
                                photo={true}
                                style={{ marginTop: 40, height: 400, width: 300, transform: [{ scale: 1.0 }] }}
                                device={dev as CameraDevice}>
                            </Camera>
                            <Text
                                style={{
                                    textAlign: "center",
                                    color: "red"
                                }}
                            >
                                {apiError}
                            </Text>
                        </>
                    ) : (
                        <>
                            <Text>
                                The De1-LoC also offers facial recognition functionality. Hit register and submit between 10 and 20 photos of your face in varying positions and lightning. Once enabled you will be able to unlock your door using only your face!
                            </Text>
                            <Text>
                                Please note that after submitting your photos it may take up to 10 minutes for your face to be learned by the system
                            </Text>
                        </>
                    )}
                </View>
                {user.profile.face_enabled ? (
                    isUnlocking ? (
                        <ActivityIndicator
                            style={{
                                marginTop: 30
                            }}
                            animating={true}
                            color="blue"
                        />
                    ) :
                        (<Button
                            style={{
                                marginTop: 30,
                                width: 100
                            }}
                            mode="contained"
                            color="blue"
                            onPress={() => {
                                setIsUnlocking(true);
                                setApiError("");
                                cameraRef.current?.takePhoto({
                                    qualityPrioritization: "speed",
                                    flash: "off",
                                }).then((snap) => {
                                    authFaceID(
                                        "file://" + snap.path,
                                        onSuccess,
                                        (e: string) => {
                                            setApiError(`Error: ${e}`);
                                            setIsUnlocking(false);
                                        });
                                });
                            }}
                        >
                            <Text>
                                Unlock
                            </Text>
                        </Button>
                        )) : (
                    <Button
                        mode="contained"
                        color="blue"
                        style={{ marginTop: 10 }}
                        onPress={() => {
                            launchImageLibrary(
                                {
                                    mediaType: "photo",
                                    selectionLimit: 20
                                },
                                (response: any) => {
                                    if (!response.didCancel) {
                                        const photos = response.assets;
                                        const files = photos.map((photo: Asset) => photo.uri)
                                        const onSuccess = () => {
                                            updateUser({
                                                ...user,
                                                profile: {
                                                    ...user.profile,
                                                    face_enabled: 1
                                                }
                                            })
                                        }
                                        const onFailure = () => {

                                        }
                                        registerFace(files, onSuccess, onFailure);
                                    }
                                }
                            )
                        }}
                    >
                        Register
                    </Button>
                )

                }

            </View>
        );
        const screen = (dev == null || !isActive) ? (
            <View
                style={{
                    height: "100%",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center"
                }}
            >
                <ActivityIndicator
                    animating={true}
                    color="blue"
                />
            </View>
        ) : camera;

        return (
            <SafeAreaView
                style={{ flexDirection: "row", alignItems: "center", justifyContent: "center", margin: 10 }}
            >
                {screen}
            </SafeAreaView>
        );
    }

export default FaceScan;