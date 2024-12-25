using UnityEngine;

namespace MathExtensions
{
    public static class MathfEx
    {
        public static float InputModulus(float value, float minValue, float maxValue)
        {
            float modulus = maxValue - minValue;

            value -= minValue;
            value %= modulus;
            value += minValue;

            return value;
        }

        public static float NormalizeAngle(float angle)
        {
            // normalize angle to -pi..pi
            return InputModulus(angle, -Mathf.PI, Mathf.PI);
        }
    }
}