/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SpellSchema } from '../models/SpellSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SpellService {

    /**
     * Get Spell
     * @param id
     * @returns SpellSchema Successful Response
     * @throws ApiError
     */
    public static getSpell(
        id: any,
    ): CancelablePromise<SpellSchema> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/spell/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
