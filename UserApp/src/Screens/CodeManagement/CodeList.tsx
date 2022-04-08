/* Relative Imports */
import CodeListItem, { CodeObject } from './CodeListItem';
import { UserState } from '../../State/UserState/UserState';
import { deleteCode, editCode } from '../../Networking/CodeManagement';
import { getCodes } from '../../Networking/UserManagement';

/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */

import { FormikValues } from 'formik';
import { SafeAreaView, ScrollView } from 'react-native';
import { Button, Title } from 'react-native-paper';
import React, { Dispatch, SetStateAction } from 'react';

const CodeList: React.FC<{
    navigation: any,
    user: UserState,
    updateUser: Dispatch<SetStateAction<UserState>>
}> = ({ navigation, user, updateUser }) => {
    const codeData = user.codes;
    const onDeleteCode = (index: number) => () => {
        const onDeleteSuccess = () => {
            const onSuccess = (codes: Object) => {
                updateUser({
                    ...user,
                    codes: Object.values(codes)
                })
            }
            const onFailure = (e: string) => console.log(e)
            getCodes(onSuccess, onFailure);
        }
        const onDeleteFailure = (e: string) => {
            console.log(e);
        }
        deleteCode(codeData[index].id as number, onDeleteSuccess, onDeleteFailure);
    }
    const onEditCode = (index: number) => (
        values: FormikValues,
        onItemSuccess: () => void,
        onItemFailure: (e: string) => void
    ) => {
        const onEditSuccess = () => {
            const onSuccess = (codes: Object) => {
                onItemSuccess();
                updateUser({
                    ...user,
                    codes: Object.values(codes)
                })
            }
            const onFailure = (e: string) => console.log(e)
            getCodes(onSuccess, onFailure);
        }
        const onEditFailure = (e: string) => {
            onItemFailure(e);
        }

        editCode({
            codename: values.codename,
            code: values.code,
            id: codeData[index].id
        }, onEditSuccess, onEditFailure
        );

    }
    return (
        <SafeAreaView
            style={{
                paddingBottom: 82
            }}
        >
            <Title
                style={{
                    textAlign: "center",
                    paddingTop: 10
                }}
            >
                Codes
            </Title>
            <ScrollView>
                {codeData.map((code: CodeObject, index: number) => (
                    <CodeListItem
                        code={code}
                        key={index}
                        editCode={onEditCode(index)}
                        onDelete={onDeleteCode(index)}
                    />
                ))}
            </ScrollView>
            <Button
                mode="contained"
                color="blue"
                onPress={() => {
                    navigation.navigate("AddCode")
                }}>
                Add new code
            </Button>
        </SafeAreaView>
    )
}

export default CodeList;