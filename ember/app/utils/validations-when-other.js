import validateWhenOther from 'outdated/validators/validate-when-other';

const validationsWhenOther = ({
  field,
  otherFieldValidator,
  fieldValidators,
}) =>
  fieldValidators.map((fv) =>
    validateWhenOther({
      field,
      otherFieldValidator,
      fieldValidator: fv,
    }),
  );
export default validationsWhenOther;
