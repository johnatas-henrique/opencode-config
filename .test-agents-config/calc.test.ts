import { add, subtract } from './calc';

describe('Calculator', () => {
  test('adds two numbers', () => {
    expect(add(1, 2)).toBe(3);
  });
  
  test('subtracts two numbers', () => {
    expect(subtract(5, 3)).toBe(2);
  });
});
