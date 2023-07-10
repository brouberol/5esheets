/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { EquippedItemSchema } from './EquippedItemSchema';
import type { PartySchema } from './PartySchema';
import type { PlayerSchema } from './PlayerSchema';

/**
 * The details of a character, excluding the player
 */
export type CharacterSchemaNoPlayer = {
    id: number;
    name: string;
    slug: string;
    class_: string;
    level: number;
    data: Record<string, any>;
    party: PartySchema;
    player: PlayerSchema;
    equipment: Array<EquippedItemSchema>;
};

