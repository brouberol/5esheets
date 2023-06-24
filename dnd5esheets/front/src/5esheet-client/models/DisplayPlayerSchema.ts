/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CharacterSchemaNoPlayer } from "./CharacterSchemaNoPlayer";

/**
 * A player details including the list of their characters
 */
export type DisplayPlayerSchema = {
  id: number;
  name: string;
  characters: Array<CharacterSchemaNoPlayer>;
};
