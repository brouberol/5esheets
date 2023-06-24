/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DisplayPlayerSchema } from '../models/DisplayPlayerSchema';
import type { UpdatePlayerSchema } from '../models/UpdatePlayerSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PlayerService {

    /**
     * Display Player
     * Display all details of a given player.
     * @param id
     * @returns DisplayPlayerSchema Successful Response
     * @throws ApiError
     */
    public static displayPlayer(
        id: number,
    ): CancelablePromise<DisplayPlayerSchema> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/player/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Player
     * Update a player details.
     *
     * Examples of JSON body paylods:
     * @param id
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updatePlayer(
        id: number,
        requestBody: UpdatePlayerSchema,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/player/{id}',
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
