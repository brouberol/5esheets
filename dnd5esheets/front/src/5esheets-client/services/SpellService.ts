/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SearchResult } from '../models/SearchResult';
import type { SpellSchema } from '../models/SpellSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SpellService {

    /**
     * Search Spells
     * @param searchTerm
     * @param favoredLanguage
     * @param limit
     * @returns SearchResult Successful Response
     * @throws ApiError
     */
    public static searchSpells(
        searchTerm: string,
        favoredLanguage?: (string | null),
        limit: number = 10,
    ): CancelablePromise<Array<SearchResult>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/spell/search',
            query: {
                'search_term': searchTerm,
                'favored_language': favoredLanguage,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Spell
     * Return all details of a given spell.
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
