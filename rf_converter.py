import sys
import joblib
import numpy as np

if len(sys.argv) != 2:
    print("Usage: python rf_converter.py ecg_random_forest.joblib")
    sys.exit(1)

model_file = sys.argv[1]
model = joblib.load(model_file)

if not hasattr(model, "estimators_"):
    raise ValueError("The file does not contain a fitted Random Forest model.")

if len(model.classes_) != 2:
    raise ValueError("This converter requires exactly 2 classes.")

trees = model.estimators_
n_trees = len(trees)

tree_data = []

for tree in trees:
    t = tree.tree_

    children_left = t.children_left
    children_right = t.children_right
    feature = t.feature
    threshold = t.threshold
    values = t.value

    nodes = len(children_left)

    left = children_left.astype(np.int32)
    right = children_right.astype(np.int32)
    feat = feature.astype(np.int16)
    thresh = threshold.astype(np.float32)

    value0 = np.zeros(nodes, dtype=np.float32)
    value1 = np.zeros(nodes, dtype=np.float32)

    for i in range(nodes):
        total = np.sum(values[i][0])

        if total > 0:
            value0[i] = values[i][0][0] / total
            value1[i] = values[i][0][1] / total

    tree_data.append(
        (left, right, feat, thresh, value0, value1)
    )

with open("ecg_model.h", "w") as f:

    f.write("#ifndef ECG_MODEL_H\n")
    f.write("#define ECG_MODEL_H\n\n")

    f.write("#include <stdint.h>\n\n")

    f.write(f"#define RF_N_TREES {n_trees}\n\n")

    for i, data in enumerate(tree_data):

        left, right, feat, thresh, value0, value1 = data

        f.write(f"static const int32_t tree_{i}_left[] = {{")
        f.write(",".join(map(str, left)))
        f.write("};\n")

        f.write(f"static const int32_t tree_{i}_right[] = {{")
        f.write(",".join(map(str, right)))
        f.write("};\n")

        f.write(f"static const int16_t tree_{i}_feature[] = {{")
        f.write(",".join(map(str, feat)))
        f.write("};\n")

        f.write(f"static const float tree_{i}_threshold[] = {{")
        f.write(",".join(f"{x:.8f}f" for x in thresh))
        f.write("};\n")

        f.write(f"static const float tree_{i}_value0[] = {{")
        f.write(",".join(f"{x:.8f}f" for x in value0))
        f.write("};\n")

        f.write(f"static const float tree_{i}_value1[] = {{")
        f.write(",".join(f"{x:.8f}f" for x in value1))
        f.write("};\n\n")

    f.write("""
static float rf_tree_predict(
    const float *features,
    const int32_t *left,
    const int32_t *right,
    const int16_t *feature,
    const float *threshold,
    const float *value0,
    const float *value1
) {
    int32_t node = 0;

    while (left[node] != -1) {

        int16_t f = feature[node];

        if (features[f] <= threshold[node])
            node = left[node];
        else
            node = right[node];
    }

    return value1[node];
}

static float rf_predict_proba(
    const float *features
) {

    float abnormal_probability = 0.0f;

""")

    for i, data in enumerate(tree_data):

        left, right, feat, thresh, value0, value1 = data

        f.write(
            f"    abnormal_probability += rf_tree_predict("
            f"features, tree_{i}_left, tree_{i}_right, "
            f"tree_{i}_feature, tree_{i}_threshold, "
            f"tree_{i}_value0, tree_{i}_value1);\n"
        )

    f.write("""
    abnormal_probability /= RF_N_TREES;

    return abnormal_probability;
}

static int rf_predict(
    const float *features
) {

    float abnormal = rf_predict_proba(features);

    if (abnormal >= 0.5f)
        return 1;

    return 0;
}

#endif
""")

print("Random Forest conversion completed.")
print("Generated file: ecg_model.h")
print("Trees:", n_trees)