/* 
 * External Library Code:
 * See README.MD  for link to documentation used for
 * interacting with these components
 */
import * as Yup from 'yup';
/* Relative Imports */
import { ERROR } from '../../utils/errors';
/* Code for Ensuring confirm password is same as password */
/* https://sagar-shrestha.medium.com/yup-validate-if-the-values-of-two-fields-are-the-same-12c1e997920 */
export const RegistrationSchema = Yup.object().shape({
    firstname: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    lastname: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    username: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    password: Yup.string().min(8, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    confirmPass: Yup.string().required(ERROR.required).oneOf([Yup.ref('password')], ERROR.mustMatch)
});

export const LoginSchema = Yup.object().shape({
    username: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required),
    password: Yup.string().min(2, ERROR.tooShort).max(64, ERROR.tooLong).required(ERROR.required)
});