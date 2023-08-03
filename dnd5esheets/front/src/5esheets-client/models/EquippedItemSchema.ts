/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ItemSchema } from './ItemSchema';

/**
 * The details of an equipped item (the association bewteen an item and a character equipment)
 */
export type EquippedItemSchema = {
    id: number;
    item: ItemSchema;
    amount: number;
    equipped: boolean;
};

