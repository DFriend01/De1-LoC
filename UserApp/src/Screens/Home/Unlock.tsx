/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React from 'react';
import { SafeAreaView, View } from 'react-native';
import { Button, TextInput, Title } from 'react-native-paper';
import { Formik, FormikValues } from 'formik';
/* Relative Imports */
import { UserState } from '../../State/UserState/UserState';
import { unlock } from '../../Networking/AuthManagement';

const initialValues = {
    code: ""
}

const Unlock: React.FC<{
    navigation: any,
    user: UserState
}> = ({ navigation, user }) => {

    const onSubmit = (values: FormikValues) => {
        const onSuccess = () => {
            console.log({ code: values.code })
            navigation.navigate("Success");
        }
        const onFailure = (e: string) => {
            console.log(e);
        }
        unlock(
            values.code,
            onSuccess,
            onFailure
        );
    }
    return (
        <SafeAreaView
            style={{ margin: 10 }}
        >
            <Title
                style={{
                    textAlign: "center"

                }}
            >
                Please enter your doorcode
            </Title>
            <Formik
                initialValues={initialValues}
                onSubmit={onSubmit}
                validateOnBlur={false}
                validateOnChange={false}
            >
                {({ handleChange, handleBlur, handleSubmit, values, errors, touched, setFieldError, resetForm }) => (
                    <>
                        <TextInput
                            label="Code"
                            value={values.code}
                            keyboardType="number-pad"
                            onBlur={handleBlur("code")}
                            activeUnderlineColor="blue"
                            onChangeText={handleChange("code")}
                        />
                        <View
                            style={{
                                flexDirection: 'row',
                                paddingTop: 10,
                                justifyContent: 'center'
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
                    </>
                )}
            </Formik>
        </SafeAreaView>
    )
}

export default Unlock;