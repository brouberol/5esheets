/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PlayerRole } from './PlayerRole';
import type { RestrictedCharacterSchema } from './RestrictedCharacterSchema';

/**
 * A player details including the list of their characters
 */
export type DisplayPlayerSchema = {
    id: number;
    name: string;
    player_roles: Array<PlayerRole>;
    characters: Array<RestrictedCharacterSchema>;
};

