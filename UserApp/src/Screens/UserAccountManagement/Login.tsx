/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React from 'react';
import { Keyboard, SafeAreaView, ScrollView, Text, View } from 'react-native';
import { Button, TextInput, Title } from 'react-native-paper'
import { Formik, FormikValues } from 'formik';
/* Relative Imports */
import { LoginSchema } from './validationSchema';
import { Log, UserState } from '../../State/UserState/UserState';
import { login } from '../../Networking/AuthManagement';
import { getCodes, getProfile, ReturnedProfileData } from '../../Networking/UserManagement';
import { SetStateCallback } from '../../Components/useStateCallback';
import { getLogs } from '../../Networking/LogManagement';

const Login: React.FC<{
    navigation: any,
    user: UserState,
    token: string
    updateUser: SetStateCallback
}> = ({ navigation, token, user, updateUser }) => {

    const [showPass, setShowPass] = React.useState(false);

    const initalValues = {
        username: "",
        password: "",
        token: ""
    }

    const onSubmit = (values: FormikValues, { resetForm }: any) => {
        Keyboard.dismiss();
        const onSuccess = () => {
            const onFetchSuccess = (s: any) => {
                navigation.navigate("Home");
                setShowPass(false);
                resetForm();
            }
            const onLogsSuccess = (s: any) => (logs: Object) => {
                console.log(Object.keys(logs))
                updateUser({
                    ...s,
                    logs: Object.values(logs),
                    logOffset: Object.keys(logs).length
                },
                    onFetchSuccess)
            }
            const onCodesSuccess = (s: any) => (codes: Object) => {
                updateUser({
                    ...s,
                    codes: Object.values(codes)
                },
                    (s: any) => {
                        getLogs(onLogsSuccess(s), onFailure)
                    })
            }
            const onFailure = (e: string) => {
                console.log(e);
            }
            const onProfileSuccess = (profile: ReturnedProfileData) => {
                updateUser({
                    ...user,
                    profile: {
                        username: profile.username,
                        firstname: profile.firstname,
                        lastname: profile.lastname,
                        face_enabled: profile.face_enabled
                    },
                },
                    (s: any) => {
                        getCodes(onCodesSuccess(s), onFailure)
                    }
                )
            };
            getProfile(onProfileSuccess, onFailure);
        }
        const onFailure = (e: string) => {
            console.log(e);
        }
        login({
            username: values.username,
            password: values.password,
            token
        }, onSuccess, onFailure)

    }

    const onSignUp = (resetForm: any) => {
        Keyboard.dismiss();
        navigation.navigate("Register");
        setShowPass(false);
        resetForm();
    }
    const onChange = (
        handleChange: any, setFieldError: any, label: string
    ) => (e: any) => {
        setFieldError(label, "");
        handleChange(label)(e);
    }

    return (
        <SafeAreaView
            style={{
                margin: 10
            }}
        >
            {/*https://stackoverflow.com/questions/29685421/hide-keyboard-in-react-native*/}
            <ScrollView
                keyboardShouldPersistTaps="handled"
            >
                <View
                >
                    <View
                        style={{ paddingBottom: 10 }}
                    >
                        <Title
                            style={{
                                textAlign: "center",
                                fontSize: 20,
                                color: "black"
                            }}
                        >
                            Welcome to the
                        </Title>
                        <Text
                            style={{
                                textAlign: "center",
                                fontSize: 36,
                                color: "black",
                                fontWeight: "bold"
                            }}
                        >
                            De1-LoC
                        </Text>
                        <Text
                            style={{
                                textAlign: "center"
                            }}
                        >
                            By HADDware
                        </Text>
                        <Title
                            style={{
                                textAlign: "center",
                                fontSize: 20,
                                color: "black",
                            }}
                        >
                            The future of security
                        </Title>
                        <Text
                            style={{
                                textAlign: "center",
                                fontSize: 20,
                                color: "black",
                                paddingTop: 30
                            }}
                        >
                            Please Login
                        </Text>
                    </View>
                    <Formik
                        initialValues={initalValues}
                        onSubmit={onSubmit}
                        validationSchema={LoginSchema}
                        validateOnBlur={false}
                        validateOnChange={false}
                    >
                        {({ handleChange, handleBlur, handleSubmit, values, errors, touched, setFieldError, resetForm }) => (
                            <>
                                <TextInput
                                    label="Username"
                                    activeUnderlineColor="blue"
                                    value={values.username}
                                    onChangeText={onChange(handleChange, setFieldError, "username")}
                                    onBlur={handleBlur("username")}
                                />
                                {(errors.username && touched.username) ? (
                                    <Text
                                        style={{
                                            color: "red",
                                            textAlign: "center"
                                        }}
                                    >
                                        {errors.username}
                                    </Text>
                                ) : <View />}
                                <TextInput
                                    label="Password"
                                    activeUnderlineColor="blue"
                                    value={values.password}
                                    onChangeText={onChange(handleChange, setFieldError, "password")}
                                    onBlur={handleBlur("password")}
                                    secureTextEntry={!showPass}
                                    right={

                                        <TextInput.Icon
                                            name={showPass ? "eye-off" : "eye"}
                                            color="blue"
                                            onPress={() => setShowPass(!showPass)}
                                        />

                                    }
                                />
                                {(errors.password && touched.password) ? (
                                    <Text
                                        style={{
                                            color: "red",
                                            textAlign: "center"
                                        }}
                                    >
                                        {errors.password}
                                    </Text>
                                ) : <View />}
                                <Button
                                    onPress={() => onSignUp(resetForm)}
                                    color="grey"
                                >
                                    <Text style={{
                                        fontSize: 12,
                                        fontWeight: "normal",
                                        color: "black"
                                    }}>
                                        Don't have an account? Sign up!
                                    </Text>
                                </Button>
                                <Button
                                    onPress={handleSubmit}
                                    mode="contained"
                                    color="blue"
                                    style={{ marginHorizontal: 40 }}
                                >
                                    Login
                                </Button>
                            </>
                        )}

                    </Formik>
                </View>
            </ScrollView>
        </SafeAreaView>
    )
}

export default Login;