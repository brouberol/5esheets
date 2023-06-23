/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DisplayPartySchema } from '../models/DisplayPartySchema';
import type { UpdatePartySchema } from '../models/UpdatePartySchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PartyService {

    /**
     * Display Party
     * Display all details of a given party.
     * @param id
     * @returns DisplayPartySchema Successful Response
     * @throws ApiError
     */
    public static displayParty(
        id: number,
    ): CancelablePromise<DisplayPartySchema> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/party/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Party
     * Update a party details.
     *
     * Examples of JSON body paylods:
     * @param id
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateParty(
        id: number,
        requestBody: UpdatePartySchema,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/party/{id}',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
