// useCounter.test.js — Unit test for the useCounter hook
// Install: npm install -D @testing-library/react@16 jest@29
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

test('increments counter', () => {
    const { result } = renderHook(() => useCounter());
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
});

test('decrements counter', () => {
    const { result } = renderHook(() => useCounter());
    act(() => result.current.decrement());
    expect(result.current.count).toBe(-1);
});

test('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5));
    act(() => result.current.increment());
    expect(result.current.count).toBe(6);
    act(() => result.current.reset());
    expect(result.current.count).toBe(5);
});
