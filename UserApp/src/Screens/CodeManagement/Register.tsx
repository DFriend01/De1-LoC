/* Relative Imports */
import { UserState } from '../../State/UserState/UserState';
import { createCode } from '../../Networking/CodeManagement';
import { getCodes } from '../../Networking/UserManagement';
import { DoorCodeSchema } from './validationSchema';
/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React, { Dispatch, SetStateAction, useState } from 'react';
import { SafeAreaView, Text, View } from 'react-native';
import { Button, TextInput } from 'react-native-paper';
import { Formik, FormikValues } from 'formik';

const onChange = (
    handleChange: any,
    setFieldError: any,
    setApiError: any,
    label: string
) => (e: any) => {
    setFieldError(label, "");
    setApiError(false);
    handleChange(label)(e);
}

const DoorCodeRegister: React.FC<{
    navigation: any,
    user: UserState,
    updateUser: Dispatch<SetStateAction<UserState>>
}> = ({ navigation, user, updateUser }) => {
    ;
    const initialValues = {
        codename: "",
        doorcode: ""
    };
    const [apiError, setApiError] = useState("");
    const [hasError, setHasError] = useState(false);
    const onSubmit = (values: FormikValues) => {
        const onSubmitSuccess = () => {
            const onSuccess = (codes: Object) => {
                updateUser({
                    ...user,
                    codes: Object.values(codes)
                })
                navigation.goBack();
            }
            const onFailure = (e: string) => console.log(e)
            getCodes(onSuccess, onFailure);

        }
        const onSubmitFailure = (e: string) => {
            setApiError(`Error: ${e}`);
            setHasError(true);
        }
        createCode(
            {
                codename: values.codename,
                code: values.doorcode
            },
            onSubmitSuccess,
            onSubmitFailure
        );
    }

    return (
        <SafeAreaView
            style={{
                margin: 10
            }}
        >
            <Formik
                initialValues={initialValues}
                onSubmit={onSubmit}
                validationSchema={DoorCodeSchema}
                validateOnBlur={false}
                validateOnChange={false}
            >
                {({ handleChange, handleBlur, handleSubmit, values, errors, touched, setFieldError, resetForm }) => (
                    <View>
                        <Text
                            style={{
                                color: "black",
                                fontSize: 16
                            }}
                        >
                            Please enter a name for this code:
                        </Text>
                        <TextInput
                            label="Code Name"
                            activeUnderlineColor='blue'
                            value={values.codename}
                            onBlur={handleBlur("codename")}
                            onChangeText={handleChange("codename")}
                        />
                        <Text
                            style={{
                                color: "red",
                                textAlign: "center"
                            }}
                        >
                            {touched.codename && errors.codename ? (
                                errors.codename
                            ) : (
                                ""
                            )}
                        </Text>
                        <Text
                            style={{
                                color: "black",
                                fontSize: 16
                            }}
                        >
                            Please enter a four digit code:
                        </Text>
                        <TextInput
                            label="Door Code"
                            keyboardType='number-pad'
                            activeUnderlineColor="blue"
                            value={values.doorcode}
                            onBlur={handleBlur("doorcode")}
                            onChangeText={
                                onChange(handleChange, 
                                (label: string, msg: string) => {},
                                setApiError,
                                "doorcode")
                            }
                        />
                        <Text
                            style={{
                                color: "red",
                                textAlign: "center"
                            }}
                        >
                            {touched.doorcode && errors.doorcode ? (
                                errors.doorcode
                            ) : (
                                ""
                            )}
                        </Text>
                        <Text
                            style={{
                                color: "red",
                                textAlign: "center",

                            }}
                        >
                            {hasError ? apiError : ""}
                        </Text>
                        <View
                            style={{
                                flexDirection: "row",
                                alignSelf: "center",
                                paddingTop: 10
                            }}
                        >


                            <Button
                                mode="contained"
                                color="blue"
                                style={{ marginRight: 5 }}
                                onPress={handleSubmit}
                            >
                                Submit
                            </Button>
                            <Button
                                mode="contained"
                                color="blue"
                                style={{ marginLeft: 5 }}
                                onPress={() => { navigation.goBack() }}
                            >
                                Cancel
                            </Button>
                        </View>
                    </View>
                )}

            </Formik>
        </SafeAreaView>
    )
}

export default DoorCodeRegister;