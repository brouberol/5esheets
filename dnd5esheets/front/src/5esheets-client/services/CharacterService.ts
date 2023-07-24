/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CharacterSchema } from '../models/CharacterSchema';
import type { CreateCharacterSchema } from '../models/CreateCharacterSchema';
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
     * Update Character
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
    public static updateCharacter(
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

    /**
     * Delete Character
     * Delete the character associated with the slug and the currently logged in player id
     * @param slug
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteCharacter(
        slug: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
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
     * Create Character
     * Create a new character, without any data nor equipment
     * @param requestBody
     * @returns CharacterSchema Successful Response
     * @throws ApiError
     */
    public static createCharacter(
        requestBody: CreateCharacterSchema,
    ): CancelablePromise<CharacterSchema> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/character/new',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
