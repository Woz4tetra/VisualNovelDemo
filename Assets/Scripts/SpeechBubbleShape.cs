using UnityEngine;
using Unity.VectorGraphics;
using System.Collections.Generic;
using System;
using System.IO;
using MathExtensions;

[Serializable]
public class TessellationOptions
{
    public float maxTanAngleDeviation = Mathf.PI / 2.0f;
    public float stepSize = 0.01f;
    public float stepDistance = 0.1f;
    public float maxCordDeviation = float.MaxValue;

    public VectorUtils.TessellationOptions ToVectorUtilsTessellationOptions()
    {
        return new VectorUtils.TessellationOptions()
        {
            MaxTanAngleDeviation = maxTanAngleDeviation,
            SamplingStepSize = stepSize,
            StepDistance = stepDistance,
            MaxCordDeviation = maxCordDeviation
        };
    }
}

[Serializable]
public class EllipseBubbleShape
{
    public float radiusX = 0.5f;
    public float radiusY = 0.5f;
    public float originX = 0.0f;
    public float originY = 0.0f;
}

class SpeechBubbleShape : MonoBehaviour
{
    [SerializeField] float strokeWidth = 1.0f;
    [SerializeField] Color fillColor = Color.white;
    [SerializeField] Color strokeColor = Color.black;
    [SerializeField] TessellationOptions tessellationOptions;
    [SerializeField] EllipseBubbleShape baseEllipse;
    [SerializeField] EllipseBubbleShape[] ellipses;
    [SerializeField] float triangleStartAngle = 300.0f;
    [SerializeField] float triangleMidAngle = 315.0f;
    [SerializeField] float triangleStopAngle = 330.0f;
    [SerializeField] float triangleLength = 0.15f;

    void Start()
    {
        DrawBubbles();
    }

    public void DrawBubbles()
    {
        string backgroundBubbles = MakeBaseBubble(baseEllipse.radiusX, baseEllipse.radiusY, true);
        string bubbles = MakeBaseBubble(baseEllipse.radiusX, baseEllipse.radiusY, false);
        foreach (var ellipse in ellipses)
        {
            backgroundBubbles += MakeSecondaryBubble(ellipse.radiusX, ellipse.radiusY, ellipse.originX, ellipse.originY, true);
            bubbles += MakeSecondaryBubble(ellipse.radiusX, ellipse.radiusY, ellipse.originX, ellipse.originY, false);
        }
        string svg =
            $@"<svg width=""100"" height=""100"" xmlns=""http://www.w3.org/2000/svg"">
            {backgroundBubbles}
            {bubbles}
            </svg>";

        SVGParser.SceneInfo sceneInfo = SVGParser.ImportSVG(new StringReader(svg));
        List<VectorUtils.Geometry> geoms = VectorUtils.TessellateScene(sceneInfo.Scene, tessellationOptions.ToVectorUtilsTessellationOptions());
        GetComponent<SpriteRenderer>().sprite = VectorUtils.BuildSprite(geoms, 1.0f, VectorUtils.Alignment.Center, Vector2.zero, 128, true);
    }

    string MakeBaseBubble(float ellipseRadiusX, float ellipseRadiusY, bool isBackground)
    {
        float shapeStrokeWidth = isBackground ? strokeWidth : 0.0f;
        Vector2 triangleStart = AngleToEllipsePoint(triangleStopAngle, ellipseRadiusX, ellipseRadiusY);
        Vector2 triangleMiddle = AngleToEllipsePoint(triangleMidAngle, ellipseRadiusX + triangleLength, ellipseRadiusY + triangleLength);
        Vector2 triangleStop = AngleToEllipsePoint(triangleStartAngle, ellipseRadiusX, ellipseRadiusY);
        float ellipseWidth = ellipseRadiusX * 2;
        float ellipseHeight = ellipseRadiusY * 2;
        return $@"
        <g>
        <path
       id=""path0""
       style=""fill:{ColorToHtml(fillColor)};fill-opacity:1;fill-rule:evenodd;stroke:{ColorToHtml(strokeColor)};stroke-width:{shapeStrokeWidth};stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;stroke-linejoin:round""
       transform=""translate({-ellipseRadiusX},{-ellipseRadiusY})""
       d=""
       M {ellipseRadiusX},0.0 
       A {ellipseRadiusX},{ellipseRadiusY} 0 0 0 0.0,{ellipseRadiusY} 
       {ellipseRadiusX},{ellipseRadiusY} 0 0 0 {ellipseRadiusX},{ellipseHeight} 
       {ellipseRadiusX},{ellipseRadiusY} 0 0 0 {triangleStart.x},{triangleStart.y} 
       L {triangleMiddle.x},{triangleMiddle.y} {triangleStop.x},{triangleStop.y} 
       A {ellipseRadiusX},{ellipseRadiusY} 0 0 0 {ellipseWidth},{ellipseRadiusY} 
       {ellipseRadiusX},{ellipseRadiusY} 0 0 0 {ellipseRadiusX},0.0 
       Z"" />
       </g>";
    }

    string MakeSecondaryBubble(float ellipseRadiusX, float ellipseRadiusY, float originX, float originY, bool isBackground)
    {
        float shapeStrokeWidth = isBackground ? strokeWidth : 0.0f;
        return $@"
        <g>
        <ellipse
            style=""fill:{ColorToHtml(fillColor)};fill-rule:evenodd;stroke:{ColorToHtml(strokeColor)};stroke-width:{shapeStrokeWidth}""
            id=""path1""
            cx=""{originX}""
            cy=""{originY}""
            rx=""{ellipseRadiusX}""
            ry=""{ellipseRadiusY}"" />
        </g>";
    }

    string ColorToHtml(Color color)
    {
        return $"#{ColorUtility.ToHtmlStringRGB(color)}";
    }

    Vector2 AngleToEllipsePoint(float angle, float radiusX, float radiusY)
    {
        angle += 90.0f;
        float angleRad = MathfEx.NormalizeAngle(angle * Mathf.Deg2Rad);
        float x = radiusX * Mathf.Cos(angleRad) + radiusX;
        float y = radiusY * Mathf.Sin(angleRad) + radiusY;
        return new Vector2(x, y);
    }
}