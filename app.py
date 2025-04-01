from flask import Flask, request, jsonify
import ast
import operator

app = Flask(__name__)

allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def eval_expr(expr):
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return allowed_operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return allowed_operators[type(node.op)](_eval(node.operand))
        else:
            raise TypeError("不支援的運算型態")
    try:
        node = ast.parse(expr, mode='eval').body
        return _eval(node)
    except Exception as e:
        return f"錯誤：{str(e)}"

@app.route('/evaluate_expression', methods=['POST'])
def evaluate_expression():
    data = request.get_json()
    expression = data.get("expression")
    result = eval_expr(expression)
    return jsonify({
        "expression": expression,
        "result": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)