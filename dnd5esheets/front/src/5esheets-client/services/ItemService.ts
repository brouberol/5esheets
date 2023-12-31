/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ItemSchema } from '../models/ItemSchema';
import type { SearchResult } from '../models/SearchResult';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ItemService {

    /**
     * Search Items
     * @param searchTerm
     * @param favoredLanguage
     * @param limit
     * @returns SearchResult Successful Response
     * @throws ApiError
     */
    public static searchItems(
        searchTerm: string,
        favoredLanguage?: (string | null),
        limit: number = 10,
    ): CancelablePromise<Array<SearchResult>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/item/search',
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
     * Get Item
     * Return all details of a given item.
     * @param id
     * @returns ItemSchema Successful Response
     * @throws ApiError
     */
    public static getItem(
        id: any,
    ): CancelablePromise<ItemSchema> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/item/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
