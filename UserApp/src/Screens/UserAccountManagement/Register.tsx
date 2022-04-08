/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React, { useState } from 'react';
import { SafeAreaView, Text, ScrollView, View, Keyboard } from 'react-native';
import { Button, TextInput, Title } from 'react-native-paper';
import { Formik, FormikValues } from 'formik';
/* Relative Imports */
import { RegistrationSchema } from './validationSchema';
import { userData, userRegister } from '../../Networking/UserManagement';

const UserRegistration: React.FC<{ navigation: any }> = ({ navigation }) => {

    const [showPass, setShowPass] = useState(false);
    const [showConf, setShowConf] = useState(false);
    const [hasError, setHasError] = useState(false);
    const [apiError, setApiError] = useState("");

    const initialValues = {
        firstname: "",
        lastname: "",
        username: "",
        password: "",
        confirmPass: "",
    };

    const onSubmit = (values: FormikValues, { resetForm }: any) => {
        setHasError(false);
        Keyboard.dismiss();
        const onSuccess = () => {
            navigation.navigate("Login");
            setShowConf(false);
            setShowPass(false);
            resetForm();
        }
        const onFailure = (message: string) => {
            setHasError(true);
            setApiError(message);
        }
        const { confirmPass, ...userData } = values;

        //registerUser(userData as userData, onSuccess, onFailure);
        userRegister(userData as userData, onSuccess, onFailure);
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
            <ScrollView keyboardShouldPersistTaps="handled">
                <Title
                    style={{
                        textAlign: "center",
                    }}
                >
                    User Registration
                </Title>


                <Text style={{
                    fontSize: 20,
                    textAlign: "center",
                    color: "black"
                }}>
                    Please enter the following details:
                </Text>
                <Formik
                    initialValues={initialValues}
                    onSubmit={onSubmit}
                    validationSchema={RegistrationSchema}
                    validateOnBlur={false}
                    validateOnChange={false}
                >
                    {({ handleChange, handleBlur, handleSubmit, values, errors, touched, setFieldError }) => (
                        <View>
                            <TextInput
                                activeUnderlineColor='blue'
                                label="First Name"
                                onBlur={handleBlur("firstname")}
                                onChangeText={onChange(handleChange, setFieldError, "firstname")}
                                value={values.firstname}
                            />
                            {(touched.firstname && errors.firstname) ? (<Text>
                                {errors.firstname}
                            </Text>) : <View />}
                            <TextInput
                                activeUnderlineColor="blue"
                                label="Last Name"
                                onBlur={handleBlur("lastname")}
                                onChangeText={onChange(handleChange, setFieldError, "lastname")}
                                value={values.lastname}
                            />
                            {(touched.lastname && errors.lastname) ? (
                                <Text
                                    style={{
                                        color: "red",
                                        textAlign: "center"
                                    }}
                                >
                                    {errors.lastname}
                                </Text>
                            ) : <View />}
                            <TextInput
                                activeUnderlineColor="blue"
                                label="Username"
                                onBlur={handleBlur("username")}
                                onChangeText={onChange(handleChange, setFieldError, "username")}
                                value={values.username}
                            />
                            {(touched.username && errors.username) ? (
                                <Text
                                    style={{
                                        color: "red",
                                        textAlign: "center"
                                    }}>
                                    {errors.username}
                                </Text>) : <View />}
                            <TextInput
                                activeUnderlineColor='blue'
                                label="Password"
                                onBlur={handleBlur("password")}
                                secureTextEntry={!showPass}
                                onChangeText={onChange(handleChange, setFieldError, "password")}
                                value={values.password}
                                right={
                                    <TextInput.Icon
                                        color="blue"
                                        name={showPass ? "eye-off" : "eye"}
                                        onPress={() => setShowPass(!showPass)}
                                    />}
                            />
                            {(touched.password && errors.password) ? (
                                <Text
                                    style={{
                                        color: "red",
                                        textAlign: "center"
                                    }}
                                >
                                    {errors.password}
                                </Text>) : <View />}
                            <TextInput
                                activeUnderlineColor='blue'
                                label="Confirm Password"
                                onBlur={handleBlur("confirmPass")}
                                secureTextEntry={!showConf}
                                onChangeText={onChange(handleChange, setFieldError, "confirmPass")}
                                value={values.confirmPass}
                                right={
                                    <TextInput.Icon
                                        color="blue"
                                        name={showConf ? "eye-off" : "eye"}
                                        onPress={() => setShowConf(!showConf)}
                                    />}
                            />
                            {(touched.confirmPass && errors.confirmPass) ? (
                                <Text
                                    style={{
                                        color: "red",
                                        textAlign: "center"
                                    }}
                                >
                                    {errors.confirmPass}
                                </Text>) : <View />}
                            {(hasError) ? (
                                <Text
                                    style={{
                                        color: "red",
                                        textAlign: "center"
                                    }}
                                >
                                    {apiError}
                                </Text>) : <View />}
                            <View
                                style={{
                                    flexDirection: "row",
                                    justifyContent: "center",
                                    alignItems: "center",
                                    paddingTop: 10
                                }}
                            >
                                <Button
                                    onPress={handleSubmit}
                                    mode="contained"
                                    color="blue"
                                    style={{ marginRight: 5 }}
                                >
                                    Submit
                                </Button>
                                <Button
                                    onPress={() => { navigation.goBack() }}
                                    mode="contained"
                                    color="blue"
                                    style={{ marginLeft: 5 }}
                                >
                                    Cancel
                                </Button>
                            </View>
                        </View>
                    )}
                </Formik>
            </ScrollView>
        </SafeAreaView>
    )
}

export default UserRegistration;