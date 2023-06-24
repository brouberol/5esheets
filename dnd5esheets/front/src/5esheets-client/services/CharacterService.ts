/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CharacterSchema } from '../models/CharacterSchema';
import type { ListCharacterSchema } from '../models/ListCharacterSchema';
import type { UpdateCharacterSchema } from '../models/UpdateCharacterSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class CharacterService {

    /**
     * List Characters
     * List all characters.
     *
     * The returned payload will not include the character sheet details.
     * @returns ListCharacterSchema Successful Response
     * @throws ApiError
     */
    public static listCharacters(): CancelablePromise<Array<ListCharacterSchema>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/character/',
        });
    }

    /**
     * Display Character
     * Display all details of a given character.
     * @param slug
     * @returns CharacterSchema Successful Response
     * @throws ApiError
     */
    public static displayCharacter(
        slug: string,
    ): CancelablePromise<CharacterSchema> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/character/{slug}',
            path: {
                'slug': slug,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update
     * Update a character details.
     *
     * Examples of JSON body paylods:
     *
     * - `{"level": 5 }`
     * - `{"name": "Toto"}`
     * - `{"class_": "Guerrier", "data": {"background": "Folk Hero"}}`
     *
     * In the last example, we update both a direct character attribute
     * as well as an attribute nested in the character JSON data.
     * @param slug
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static update(
        slug: string,
        requestBody: UpdateCharacterSchema,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/character/{slug}',
            path: {
                'slug': slug,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
