/* Relative Imports */
import { EditCodeSchema } from './validationSchema';
/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import React, { useState } from 'react';
import { Text, View } from 'react-native';
import { Button, IconButton, TextInput } from 'react-native-paper';
import { Formik, FormikValues } from 'formik';

export interface CodeObject {
    id?: number;
    codename: string;
    code: string;
};

const CodeListItem: React.FC<{
    code: CodeObject,
    editCode: (
        values: FormikValues,
        onItemSuccess: () => void,
        onItemFailure: (e: string) => void
    ) => void,
    onDelete: () => void,

}> = ({ code, editCode, onDelete }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [apiError, setApiError] = useState("");
    const onSuccess = () => {
        setApiError("");
        setIsEditing(false);
    }
    const onFailure = (e: string) => {
        setApiError(`Error: ${e}`);
    } 
    const onSubmit = (values: FormikValues) => {
        editCode(values, onSuccess, onFailure);
    }
    return (
        <View
            style={{
                borderColor: "blue",
                borderWidth: 4,
                backgroundColor: "lightskyblue",
                margin: 5,
                borderRadius: 5
            }}
        >
            <Formik
                initialValues={code}
                onSubmit={onSubmit}
                validateOnBlur={false}
                validationSchema={EditCodeSchema}
                validateOnChange={false}
            >
                {({ handleBlur, handleChange, handleSubmit, values, touched, errors }) => (
                    <>
                        <TextInput
                            disabled={!isEditing}
                            activeUnderlineColor={"blue"}
                            label="Code Name"
                            value={values.codename}
                            onBlur={handleBlur("codename")}
                            onChangeText={handleChange("codename")}
                        />
                        <TextInput
                            disabled={!isEditing}
                            activeUnderlineColor={"blue"}
                            label={"Code"}
                            value={values.code}
                            onBlur={handleBlur("code")}
                            onChangeText={handleChange("code")}
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
                                color: "red",
                                textAlign: "center"
                            }}
                        >
                            {touched.code && errors.code ? (
                                errors.code
                            ) : (
                                ""
                            )}
                        </Text>
                        <Text   
                            style={{
                                color: "red",
                                textAlign: "center"
                            }}
                        >
                            {apiError}
                        </Text>
                        <View
                            style={{
                                flexDirection: "row",
                                alignItems: "center",
                                justifyContent: "flex-end"
                            }}
                        >

                            <Button
                                onPress={isEditing ? handleSubmit : () => { setIsEditing(true) }}
                                color="blue"
                                mode="contained"
                                style={{
                                    width: 75
                                }}
                            >
                                <Text>
                                {isEditing ? "Save" : "Edit"}
                                </Text>
                            </Button>

                            <IconButton
                                icon="delete"
                                onPress={onDelete}
                            />
                        </View>
                    </>
                )}
            </Formik>
        </View>
    );
}

export default CodeListItem;
