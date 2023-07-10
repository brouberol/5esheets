/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_login_for_access_token } from '../models/Body_login_login_for_access_token';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class LoginService {

    /**
     * Login For Access Token
     * Submit a player's username and password to login.
     *
     * If the password verifies, returns a JWT usable to communicate with the API.
     * If not, raise a 401 error.
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static loginForAccessToken(
        formData: Body_login_login_for_access_token,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/login/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
